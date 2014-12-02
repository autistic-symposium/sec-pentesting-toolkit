# SHA2 family Python 2 implementation
# Copyright (C) 2013  Filippo Valsorda
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import struct
import binascii
import math

rrot = lambda x, n: (x >> n) | (x << (32 - n))

from itertools import count, islice
primes = lambda n: islice((k for k in count(2) if all(k % d for d in range(2, k))), 0, n)

class _SHA2_32():

    # (first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311)
    _k = [int(math.modf(x ** (1.0/3))[0] * (1 << 32)) for x in primes(64)]

    def __init__(self, message):
        length = struct.pack('>Q', len(message) * 8)
        while len(message) > 64:
            self._handle(message[:64])
            message = message[64:]
        message += '\x80'
        message += '\x00' * ((56 - len(message) % 64) % 64)
        message += length
        while len(message):
            self._handle(message[:64])
            message = message[64:]

    def _handle(self, chunk):
        w = list(struct.unpack('>' + 'I' * 16, chunk))

        for i in range(16, 64):
            s0 = rrot(w[i - 15], 7) ^ rrot(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = rrot(w[i - 2], 17) ^ rrot(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & 0xffffffff)

        a = self._h0
        b = self._h1
        c = self._h2
        d = self._h3
        e = self._h4
        f = self._h5
        g = self._h6
        h = self._h7

        for i in range(64):
            S1 = rrot(e, 6) ^ rrot(e, 11) ^ rrot(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp = h + S1 + ch + self._k[i] + w[i]
            d = (d + temp) & 0xffffffff
            S0 = rrot(a, 2) ^ rrot(a, 13) ^ rrot(a, 22)
            maj = (a & (b ^ c)) ^ (b & c)
            temp = (temp + S0 + maj) & 0xffffffff

            h, g, f, e, d, c, b, a = g, f, e, d, c, b, a, temp

        self._h0 = (self._h0 + a) & 0xffffffff
        self._h1 = (self._h1 + b) & 0xffffffff
        self._h2 = (self._h2 + c) & 0xffffffff
        self._h3 = (self._h3 + d) & 0xffffffff
        self._h4 = (self._h4 + e) & 0xffffffff
        self._h5 = (self._h5 + f) & 0xffffffff
        self._h6 = (self._h6 + g) & 0xffffffff
        self._h7 = (self._h7 + h) & 0xffffffff

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode()


class SHA2_256(_SHA2_32):

    # (first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19)
    _h0, _h1, _h2, _h3, _h4, _h5, _h6, _h7 = (
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)

    def digest(self):
        return struct.pack('>IIIIIIII', self._h0, self._h1, self._h2,
                           self._h3, self._h4, self._h5, self._h6, self._h7)

class SHA2_224(_SHA2_32):

    # (second 32 bits of the fractional parts of the square roots of the 9..16 primes 23..53)
    _h0, _h1, _h2, _h3, _h4, _h5, _h6, _h7 = (
        0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939,
        0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4)

    def digest(self):
        return struct.pack('>IIIIIII', self._h0, self._h1, self._h2,
                           self._h3, self._h4, self._h5, self._h6)


class _SHA2_64():

    # (first 64 bits of the fractional parts of the cube roots of the first 80 primes)
    _k = [int(math.modf(x ** (1.0/3))[0] * (1 << 80)) for x in primes(80)]

    def __init__(self, message):
        length = struct.pack('>QQ', (len(message) * 8) >> 32, (len(message) * 8) & 0xffffffff)
        while len(message) > 128:
            self._handle(message[:128])
            message = message[128:]
        message += '\x80'
        message += '\x00' * ((112 - len(message) % 128) % 128)
        message += length
        while len(message):
            self._handle(message[:128])
            message = message[128:]

    def _handle(self, chunk):
        w = list(struct.unpack('>' + 'Q' * 16, chunk))

        for i in range(16, 80):
            s0 = rrot(w[i - 15], 7) ^ rrot(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = rrot(w[i - 2], 17) ^ rrot(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & 0xffffffffffffffff)

        a = self._h0
        b = self._h1
        c = self._h2
        d = self._h3
        e = self._h4
        f = self._h5
        g = self._h6
        h = self._h7

        for i in range(80):
            S1 = rrot(e, 6) ^ rrot(e, 11) ^ rrot(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp = h + S1 + ch + self._k[i] + w[i]
            d = (d + temp) & 0xffffffffffffffff
            S0 = rrot(a, 2) ^ rrot(a, 13) ^ rrot(a, 22)
            maj = (a & (b ^ c)) ^ (b & c)
            temp = (temp + S0 + maj) & 0xffffffffffffffff

            h, g, f, e, d, c, b, a = g, f, e, d, c, b, a, temp

        self._h0 = (self._h0 + a) & 0xffffffffffffffff
        self._h1 = (self._h1 + b) & 0xffffffffffffffff
        self._h2 = (self._h2 + c) & 0xffffffffffffffff
        self._h3 = (self._h3 + d) & 0xffffffffffffffff
        self._h4 = (self._h4 + e) & 0xffffffffffffffff
        self._h5 = (self._h5 + f) & 0xffffffffffffffff
        self._h6 = (self._h6 + g) & 0xffffffffffffffff
        self._h7 = (self._h7 + h) & 0xffffffffffffffff

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode()


class SHA2_512(_SHA2_64):

    # (first 64 bits of the fractional parts of the square roots of the first 8 primes 2..19)
    _h0, _h1, _h2, _h3, _h4, _h5, _h6, _h7 = (
        0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b,
        0xa54ff53a5f1d36f1, 0x510e527fade682d1, 0x9b05688c2b3e6c1f,
        0x1f83d9abfb41bd6b, 0x5be0cd19137e2179)

    def digest(self):
        return struct.pack('>QQQQQQQQ', self._h0, self._h1, self._h2,
                           self._h3, self._h4, self._h5, self._h6, self._h7)


class SHA2_384(_SHA2_64):

    # (second 64 bits of the fractional parts of the square roots of the 9..16 primes 23..53)
    _h0, _h1, _h2, _h3, _h4, _h5, _h6, _h7 = (
        0xcbbb9d5dc1059ed8, 0x629a292a367cd507, 0x9159015a3070dd17,
        0x152fecd8f70e5939, 0x67332667ffc00b31, 0x8eb44a8768581511,
        0xdb0c2e0d64f98fa7, 0x47b5481dbefa4fa4)

    def digest(self):
        return struct.pack('>QQQQQQQ', self._h0, self._h1, self._h2,
                           self._h3, self._h4, self._h5, self._h6)
