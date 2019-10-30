# PyGenere v 0.3
#
# Release Date: 2007-02-16
# Author: Simon Liu <webmonkey at smurfoncrack dot com>
# URL: http://smurfoncrack.com/pygenere
# History and License at end of file


r"""
This library implements the Caesar and Vigenere ciphers, allowing a piece of
plaintext to be encoded using a numeric rotation or an alphabetic keyword,
and also decoded if the key/rotation is known.

In case the key is not known, methods are provided that analyze the ciphertext
and attempt to find the original key and decode the message: these work using
character frequency analysis.  English, French, German, Italian, Portuguese,
and Spanish texts are currently supported.  Results are generally accurate if
the length of the plaintext is long compared to the length of the key used to
encipher it.

Example usage:

>>> from pygenere import *
>>> plaintext = 'Attack at dawn.'
>>> key = 3
>>> ciphertext = Caesar(plaintext).encipher(key)
>>> ciphertext
'Dwwdfn dw gdzq.'
>>> Vigenere(ciphertext).decipher('D')    # A=0, B=1, C=2, D=3, etc.
'Attack at dawn.'

The 'Attack at dawn.' message is too short for the automatic Vigenere decoder
to work properly.  A way around this is to concatenate copies of the message
to itself, increasing the amount of text to analyze:

>>> VigCrack(ciphertext*5).crack_codeword(1)
'D'
>>> VigCrack(ciphertext*5).crack_message()
'Attack at dawn.Attack at dawn.Attack at dawn.Attack at dawn.Attack at dawn.'

The crack_message() and crack_codeword() methods in the VigCrack class take 0,
1 or 2 arguments.  For more information, see the docstrings for those methods.

Note that this method (repeating the ciphertext) does not always work, but can
sometimes be of use, as in the case of the example above.

Both the encipher() and decipher() methods for Vigenere and Caesar objects
return a cipher object of the same type.  This makes method chaining possible:

>>> codeword = 'King'
>>> Vigenere(plaintext).encipher(codeword).decipher(codeword)
'Attack at dawn.'
>>> Caesar(plaintext).encipher(3).decipher(2).decipher(1)
'Attack at dawn.'

Note:

  1. Non-alphabetic input (e.g. " " and "." above) is left as is.
  2. The case of the input (plaintext/ciphertext) is preserved.
  3. The case of the key doesn't matter, e.g. 'king', 'KING', and 'KiNg' are
     identical keys.

Since each cipher is a subclass of the built-in str class, any cipher object
can be treated as a string.  For instance:

>>> Vigenere(plaintext).replace(' ', '').lower()
'attackatdawn.'

However, since Python 2.1 and below don't seem to support subclasses of
the str class, Python 2.2 or newer is required to use this library.

By default, PyGenere assumes that the original plaintext message was written
in English, and thus English character frequencies are used for analysis.
To change the language, the set_language() method is used.  For example, the
following code shows a short French string, encrypted with the keyword
'FR', decoded.  Without setting the language first, an incorrect result is
obtained:

>>> text = 'Non, je ne veux pas coucher avec vous ce soir'
>>> encrypted = Vigenere(text).encipher('FR')
>>> print VigCrack(encrypted).set_language('FR').crack_codeword(2)
FR
>>> print VigCrack(encrypted).crack_codeword(2)
FS

This isn't always the case: two languages may have similar enough character
frequency distributions that decoding sometimes works correctly even when the
language setting is incorrect.

Currently, PyGenere's language options other than English are DE (German),
ES (Spanish), FR (French), IT (Italian), and PT (Portuguese).
"""


class Caesar(str):

    """An implementation of the Caesar cipher."""

    def encipher(self, shift):
        """Encipher input (plaintext) using the Caesar cipher and return it
           (ciphertext)."""
        ciphertext = []
        for p in self:
            if p.isalpha():
                ciphertext.append(chr((ord(p) - ord('Aa'[int(p.islower())]) +
                shift) % 26 + ord('Aa'[int(p.islower())])))
            else:
                ciphertext.append(p)
        return Caesar(''.join(ciphertext))

    def decipher(self, shift):
        """Decipher input (ciphertext) using the Caesar cipher and return it
           (plaintext)."""
        return self.encipher(-shift)


class Vigenere(str):

    """An implementation of the Vigenere cipher."""

    def encipher(self, key):
        """Encipher input (plaintext) using the Vigenere cipher and return
           it (ciphertext)."""
        ciphertext = []
        k = 0
        n = len(key)
        for i in range(len(self)):
            p = self[i]
            if p.isalpha():
                ciphertext.append(chr((ord(p) + ord(
                (key[k % n].upper(), key[k % n].lower())[int(p.islower())]
                ) - 2*ord('Aa'[int(p.islower())])) % 26 +
                ord('Aa'[int(p.islower())])))
                k += 1
            else:
                ciphertext.append(p)
        return Vigenere(''.join(ciphertext))

    def decipher(self, key):
        """Decipher input (ciphertext) using the Vigenere cipher and return
           it (plaintext)."""
        plaintext = []
        k = 0
        n = len(key)
        for i in range(len(self)):
            c = self[i]
            if c.isalpha():
                plaintext.append(chr((ord(c) - ord(
                (key[k % n].upper(), key[k % n].lower())[int(c.islower())]
                )) % 26 + ord('Aa'[int(c.islower())])))
                k += 1
            else:
                plaintext.append(c)
        return Vigenere(''.join(plaintext))


class InputError(Exception):

    """This class is only used for throwing exceptions if the user supplies
       invalid input (e.g. ciphertext is an empty string)."""

    pass


class VigCrack(Vigenere):

    """
    VigCrack objects have methods to break Vigenere-encoded texts when the
    original key is unknown.

    The technique used is based on the one described in:

    http://www.stonehill.edu/compsci/Shai_papers/RSA.pdf
    (pages 9-10)

    Character frequencies taken from:
    http://www.csm.astate.edu/~rossa/datasec/frequency.html (English)
    http://www.characterfrequency.com/ (French, Italian, Portuguese, Spanish)
    http://www.santacruzpl.org/readyref/files/g-l/ltfrqger.shtml (German)
    """

    # Unless otherwise specified, test for codewords between (and including)
    # these two lengths:
    __default_min_codeword_length = 5
    __default_max_codeword_length = 9

    # The following are language-specific data on character frequencies.
    # Kappa is the "index of coincidence" described in the cryptography paper
    # (link above).
    __english_data = {
                      'A':8.167, 'B':1.492, 'C':2.782, 'D':4.253, 'E':12.702,
                      'F':2.228, 'G':2.015, 'H':6.094, 'I':6.996, 'J':0.153,
                      'K':0.772, 'L':4.025, 'M':2.406, 'N':6.749, 'O':7.507,
                      'P':1.929, 'Q':0.095, 'R':5.987, 'S':6.327, 'T':9.056,
                      'U':2.758, 'V':0.978, 'W':2.360, 'X':0.150, 'Y':1.974,
                      'Z':0.074, 'max_val':12.702, 'kappa':0.0667
                     }

    __french_data = {
                     'A':8.11, 'B':0.903, 'C':3.49, 'D':4.27, 'E':17.22,
                     'F':1.14, 'G':1.09, 'H':0.769, 'I':7.44, 'J':0.339,
                     'K':0.097, 'L':5.53, 'M':2.89, 'N':7.46, 'O':5.38,
                     'P':3.02, 'Q':0.999, 'R':7.05, 'S':8.04, 'T':6.99,
                     'U':5.65, 'V':1.30, 'W':0.039, 'X':0.435, 'Y':0.271,
                     'Z':0.098, 'max_val':17.22, 'kappa':0.0746
                    }

    __german_data = {
                     'A':6.506, 'B':2.566, 'C':2.837, 'D':5.414, 'E':16.693,
                     'F':2.044, 'G':3.647, 'H':4.064, 'I':7.812, 'J':0.191,
                     'K':1.879, 'L':2.825, 'M':3.005, 'N':9.905, 'O':2.285,
                     'P':0.944, 'Q':0.055, 'R':6.539, 'S':6.765, 'T':6.742,
                     'U':3.703, 'V':1.069, 'W':1.396, 'X':0.022, 'Y':0.032,
                     'Z':1.002, 'max_val':16.693, 'kappa':0.0767
                    }

    __italian_data = {
                      'A':11.30, 'B':0.975, 'C':4.35, 'D':3.80, 'E':11.24,
                      'F':1.09, 'G':1.73, 'H':1.02, 'I':11.57, 'J':0.035,
                      'K':0.078, 'L':6.40, 'M':2.66, 'N':7.29, 'O':9.11,
                      'P':2.89, 'Q':0.391, 'R':6.68, 'S':5.11, 'T':6.76,
                      'U':3.18, 'V':1.52, 'W':0.00, 'X':0.024, 'Y':0.048,
                      'Z':0.958, 'max_val':11.57, 'kappa':0.0733
                     }

    __portuguese_data = {
                         'A':13.89, 'B':0.980, 'C':4.18, 'D':5.24, 'E':12.72,
                         'F':1.01, 'G':1.17, 'H':0.905, 'I':6.70, 'J':0.317,
                         'K':0.0174, 'L':2.76, 'M':4.54, 'N':5.37, 'O':10.90,
                         'P':2.74, 'Q':1.06, 'R':6.67, 'S':7.90, 'T':4.63,
                         'U':4.05, 'V':1.55, 'W':0.0104, 'X':0.272, 'Y':0.0165,
                         'Z':0.400, 'max_val':13.89, 'kappa':0.0745
                        }

    __spanish_data = {
                      'A':12.09, 'B':1.21, 'C':4.20, 'D':4.65, 'E':13.89,
                      'F':0.642, 'G':1.11, 'H':1.13, 'I':6.38, 'J':0.461,
                      'K':0.038, 'L':5.19, 'M':2.86, 'N':7.23, 'O':9.58,
                      'P':2.74, 'Q':1.37, 'R':6.14, 'S':7.43, 'T':4.49,
                      'U':4.53, 'V':1.05, 'W':0.011, 'X':0.124, 'Y':1.14,
                      'Z':0.324, 'max_val':13.89, 'kappa':0.0766
                     }

    # The default language is set to English.
    __lang = 'EN'
    __lang_data = __english_data

    # This method sets the lang (__lang) attribute of a VigCrack object.
    def set_language(self, language):
        self.__lang = language.upper()
        if self.__lang == 'DE':
            self.__lang_data = self.__german_data
        elif self.__lang == 'ES':
            self.__lang_data = self.__spanish_data
        elif self.__lang == 'FR':
            self.__lang_data = self.__french_data
        elif self.__lang == 'IT':
            self.__lang_data = self.__italian_data
        elif self.__lang == 'PT':
            self.__lang_data = self.__portuguese_data
        else:
            self.__lang = 'EN'
        return self

    # Rotate text n places to the right, wrapping around at the end.
    def __rotate_right(self, n):
        cutting_point = len(self) - (n % len(self))
        return self[cutting_point:] + self[:cutting_point]

    # Get every nth char from a piece of text, from a given starting position.
    def __get_every_nth_char(self, start, n):
        accumulator = []
        for i in range(len(self)):
            if (i % n) == start:
                accumulator.append(self[i])
        return VigCrack(''.join(accumulator)).set_language(self.__lang)

    # Build a dictionary containing the number of occurrences of each char.
    def __count_char_freqs(self):
        dictionary = {}
        self = self.upper()
        for char in self:
            if char.isalpha():
                dictionary[char] = dictionary.get(char, 0) + 1
        return dictionary

    # Scale the dictionary so that it can be compared with __lang_data.
    def __scale(self, dictionary):
        v = dictionary.values()
        v.sort()
        max_val = v[-1]
        scaling_factor = self.__lang_data['max_val']/max_val
        for (k, v) in dictionary.items():
            dictionary[k] = v*scaling_factor
        return dictionary

    # The residual error is the difference between a char's frequency in
    # __lang_data and its frequency in the scaled dictionary from above.
    # The error is then squared to remove a possible negative value.
    def __sum_residuals_squared(self, dictionary):
        sum = 0
        for (k, v) in dictionary.items():
            sum += (v - self.__lang_data[k])**2
        return sum

    # Find the Caesar shift that brings the ciphertext closest to the
    # character distribution of the plaintext's language.
    def __find_best_caesar_shift(self):
        best = 0
        smallest_sum = -1
        # Find the residual sum for each shift.
        for shift in range(26):
            encoded_text = Caesar(self).encipher(shift)
            vigcrack_obj = VigCrack(encoded_text).set_language(self.__lang)
            char_freqs = vigcrack_obj.__count_char_freqs()
            scaled = vigcrack_obj.__scale(char_freqs)
            current_sum = vigcrack_obj.__sum_residuals_squared(scaled)
            # Keep track of the shift with the lowest residual sum.
            # If there's a tie, the smallest shift wins.
            if smallest_sum == -1:
                smallest_sum = current_sum
            if current_sum < smallest_sum:
                best = shift
                smallest_sum = current_sum
        return best

    def __find_codeword_length(self, min_length, max_length):
        codeword_length = min_length
        kappas = []
        # Put the kappa value for each codeword length tested into an array.
        for i in range(min_length, max_length + 1):
            temp = self.__rotate_right(i)
            coincidences = 0
            for j in range(len(self)):
                if temp[j] == self[j]:
                    coincidences += 1
            kappas.append(float(coincidences)/len(self))
        # Find out which value of kappa is closest to the kappa of the
        # plaintext's language.  If there's a tie, the shortest codeword wins.
        smallest_squared_diff = -1
        for i in range((max_length + 1) - min_length):
            current_squared_diff = (self.__lang_data['kappa'] - kappas[i])**2
            if smallest_squared_diff == -1:
                smallest_squared_diff = current_squared_diff
            if current_squared_diff < smallest_squared_diff:
                codeword_length = min_length + i
                smallest_squared_diff = current_squared_diff
        return codeword_length

    def __find_codeword(self, min_length, max_length):
        # Strip away invalid chars.
        accumulator = []
        for char in self:
            if char.isalpha():
                accumulator.append(char)
        alpha_only = VigCrack(''.join(accumulator)).set_language(self.__lang)
        codeword_length = alpha_only.__find_codeword_length(min_length,
                                                            max_length)
        # Build the codeword by finding one character at a time.
        codeword = []
        for i in range(codeword_length):
            temp = alpha_only.__get_every_nth_char(i, codeword_length)
            shift = temp.__find_best_caesar_shift()
            if shift == 0:
                codeword.append('A')
            else:
                codeword.append(chr(ord('A') + (26 - shift)))
        return VigCrack(''.join(codeword)).set_language(self.__lang)

    def __parse_args(self, *arg_list):
        if len(arg_list) == 0:    # Use default values for codeword length.
            min_length = self.__default_min_codeword_length
            max_length = self.__default_max_codeword_length
        elif len(arg_list) == 1:    # Exact codeword length specified by user.
            min_length = max_length = int(arg_list[0])
        else:    # min_length and max_length given by user.
            min_length = int(arg_list[0])
            max_length = int(arg_list[1])
        # Check for input errors.
        if min_length == max_length:
            if min_length < 1:
                raise InputError('Codeword length is too small')
        else:
            if min_length < 1:
                raise InputError('min_length is too small')
            if max_length < 1:
                raise InputError('max_length is too small')
        if max_length < min_length:
            raise InputError('max_length cannot be shorter than min_length')
        if len(self) == 0:
            raise InputError('Ciphertext is empty')
        if len(self) < max_length:
            raise InputError('Ciphertext is too short')
        # Check that the ciphertext contains at least one valid character.
        has_valid_char = False
        for char in self:
            if char.isalpha():
                has_valid_char = True
                break
        if not has_valid_char:
            raise InputError('No valid characters in ciphertext')
        # If everything's all right, return the min_length and max_length.
        return [min_length, max_length]

    def crack_codeword(self, *arg_list):
        """
        Try to find the codeword that encrypted the ciphertext object.
        If no arguments are supplied, codewords between the default minimum
        length and the default maximum length are tried.
        If one integer argument is supplied, only codewords with that length
        will be tried.
        If two integer arguments are given then the first argument is treated
        as a minimum codeword length, and the second argument is treated as a
        maximum codeword length, to try.
        """
        array = self.__parse_args(*arg_list)
        return self.__find_codeword(array[0], array[1])

    def crack_message(self, *arg_list):
        """
        Try to decode the ciphertext object.
        This method accepts arguments in the same way as the crack_codeword()
        method.
        """
        codeword = self.crack_codeword(*arg_list)
        return self.decipher(codeword)


# History
# -------
#
# 2007-02-16: v 0.3. Minor (mostly cosmetic) modifications to make the code
#                    more compliant with the Python Style Guide
#                    (http://www.python.org/dev/peps/pep-0008/).
#
# 2006-06-11: v 0.2. Language support added for German (DE), Spanish (ES),
#                    French (FR), Italian (IT), and Portuguese (PT).
#
# 2006-04-29: v 0.1. First release.
#
#
#
# License
# -------
#
# Copyright (c) 2006, Simon Liu <webmonkey at smurfoncrack dot com>
# All rights reserved.
#
# This library incorporates code from the PyCipher project on SourceForge.net
# (http://sourceforge.net/projects/pycipher/).  The original copyright notice
# is preserved below as required; these modifications are released under the
# same terms.
#
#
# Copyright (c) 2005, Aggelos Orfanakos <csst0266atcsdotuoidotgr>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.