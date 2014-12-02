#!/usr/bin/python2

import os, socket, struct, sys
from Crypto.Cipher import AES


class EncryptedStream(object):
  key = 'this is not the flag nor the key'[:16]

  def __init__(self, host, port):
    self.sock = socket.socket()
    self.sock.connect((host, port))

  def send(self, msg):
    while len(msg) % 16:
      msg += '\0'

    iv = os.urandom(16)
    aes = AES.new(self.key, AES.MODE_ECB, iv)
    enc = aes.encrypt(msg)

    self.sock.send(struct.pack('<I', len(enc)))
    self.sock.send(enc)

  def recv(self, nbytes):
    return self.sock.recv(nbytes)




client = '''\
HELLO
SHOW VERSION
SET example This tiny script is basically a RedisStore...
GET example
SHOW KEYS
SET brucefact#1 Bruce Schneier can break elliptic curve cryptography by bending it into a circle
SET brucefact#2 Bruce Schneier always cooks his eggs scrambled. When he wants hardboiled eggs, he unscrambles them
SET brucefact#3 Bruce Schneier could solve this by inverting md5 hash of the flag
ENCRYPTION HEX
MD5 flag
'''

stream = EncryptedStream(sys.argv[1], int(sys.argv[2]))
stream.send(client)

while 1:
  data = stream.recv(1000)
  if not data: break
  sys.stdout.write(data)
