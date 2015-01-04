# MD4 Python 2 implementation
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
#
# Originally based, even if no code survives, on a LGPL work by
# Dmitry Rozmanov <dima@xenon.spb.ru> 2002
# http://www.geocities.com/rozmanov/python/

import struct
import binascii

lrot = lambda x, n: (x << n) | (x >> (32 - n))


class MD4():

    A, B, C, D = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476)
    buf = [0x00] * 64

    _F = lambda self, x, y, z: ((x & y) | (~x & z))
    _G = lambda self, x, y, z: ((x & y) | (x & z) | (y & z))
    _H = lambda self, x, y, z: (x ^ y ^ z)

    def __init__(self, message):
        length = struct.pack('<Q', len(message) * 8)
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
        X = list(struct.unpack('<' + 'I' * 16, chunk))
        A, B, C, D = self.A, self.B, self.C, self.D

        for i in range(16):
            k = i
            if i % 4 == 0:
                A = lrot((A + self._F(B, C, D) + X[k]) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._F(A, B, C) + X[k]) & 0xffffffff, 7)
            elif i % 4 == 2:
                C = lrot((C + self._F(D, A, B) + X[k]) & 0xffffffff, 11)
            elif i % 4 == 3:
                B = lrot((B + self._F(C, D, A) + X[k]) & 0xffffffff, 19)

        for i in range(16):
            k = (i // 4) + (i % 4) * 4
            if i % 4 == 0:
                A = lrot((A + self._G(B, C, D) + X[k] + 0x5a827999) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._G(A, B, C) + X[k] + 0x5a827999) & 0xffffffff, 5)
            elif i % 4 == 2:
                C = lrot((C + self._G(D, A, B) + X[k] + 0x5a827999) & 0xffffffff, 9)
            elif i % 4 == 3:
                B = lrot((B + self._G(C, D, A) + X[k] + 0x5a827999) & 0xffffffff, 13)

        order = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        for i in range(16):
            k = order[i]
            if i % 4 == 0:
                A = lrot((A + self._H(B, C, D) + X[k] + 0x6ed9eba1) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._H(A, B, C) + X[k] + 0x6ed9eba1) & 0xffffffff, 9)
            elif i % 4 == 2:
                C = lrot((C + self._H(D, A, B) + X[k] + 0x6ed9eba1) & 0xffffffff, 11)
            elif i % 4 == 3:
                B = lrot((B + self._H(C, D, A) + X[k] + 0x6ed9eba1) & 0xffffffff, 15)

        self.A = (self.A + A) & 0xffffffff
        self.B = (self.B + B) & 0xffffffff
        self.C = (self.C + C) & 0xffffffff
        self.D = (self.D + D) & 0xffffffff

    def digest(self):
        return struct.pack('<IIII', self.A, self.B, self.C, self.D)

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode()
