#!/usr/bin/env python

from paillier import *

print "Generating keypair..."
priv, pub = generate_keypair(512)

x = 3
print "x =", x
print "Encrypting x..."
cx = encrypt(pub, x)
print "cx =", cx

y = 5
print "y =", y
print "Encrypting y..."
cy = encrypt(pub, y)
print "cy =", cy

print "Computing cx + cy..."
cz = e_add(pub, cx, cy)
print "cz =", cz

print "Decrypting cz..."
z = decrypt(priv, pub, cz)
print "z =", z

print "Computing decrypt((cz + 2) * 3) ..."
print "result =", decrypt(priv, pub,
                          e_mul_const(pub, e_add_const(pub, cz, 2), 3))
