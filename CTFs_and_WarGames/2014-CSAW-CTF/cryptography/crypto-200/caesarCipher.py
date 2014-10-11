#!/usr/bin/env python


__author__ = "bt3gl"


import string


FREQ_ENGLISH = [0.0749, 0.0129, 0.0354, 0.0362, 0.1400, 0.0218, 0.0174, 0.0422, 0.0665, 0.0027, 0.0047, 0.0357,0.0339, 0.0674, 0.0737, 0.0243, 0.0026, 0.0614, 0.0695, 0.0985, 0.0300, 0.0116, 0.0169, 0.0028, 0.0164, 0.0004]



def delta(freq_word, freq_eng):
    # zip together the value from the text and the value from FREQ_EdiffGlist_freqISH
    diff = 0.0
    for a, b in zip(freq_word, freq_eng):
        diff += abs(a - b)
    return diff



def cipher(msg, key):
    # Make the cipher
    dec = ''
    for c in msg.lower():
        if 'a' <= c <= 'z':
             dec += chr(ord('a') + (ord(c) - ord('a') + key) % 26)
        else:
             dec += c
    return dec



def frequency(msg):
    # Compute the word frequencies
    dict_freq = dict([(c,0) for c in string.lowercase])
    diff = 0.0
    for c in msg.lower():
        if 'a'<= c <= 'z':
            diff += 1
            dict_freq[c] += 1
    list_freq = dict_freq.items()
    list_freq.sort()
    return [b / diff for (a, b) in list_freq]



def decipher(msg):
    # Decipher by frequency
    min_delta, best_rotation = 20, 0.0
    freq = frequency(msg)
    for k in range(26):
    	d = delta(freq[k:] + freq[:k], FREQ_ENGLISH)
        if d < min_delta:
            min_delta = d
            best_rotation = k
    return cipher(msg, -best_rotation)



def decipher_simple(msg):
    # very smart way of solving using translate and maketrans methods
    diff = (ord('t') - ord(s[0])) % 26
    x = string.ascii_lowercase
    x = x[diff:] + x[:diff]
    ans = string.translate(s,string.maketrans(string.ascii_lowercase,x))
    return ans



if __name__ == '__main__':

    # creating a cipher
    key = 13
    text = 'hacker school is awesome!'
    cipe = cipher(text, key)
    print "Cipher: " + cipe
  
    # decyphering
    with open('cipher.txt', 'r') as f:	
	cip = f.readlines()
	cip = cip[0].strip()
        cipe =  decipher(cip)    	  	
    	print "Decipher: " + cipe

    	
