#!/usr/bin/python2

import hashlib, os, signal, struct, sys
from Crypto.Cipher import AES


key = 'this is not the flag nor the key'[:16]
db = { }


def md5(data):
  return hashlib.md5(data).digest()


def decrypt(data):
  iv = os.urandom(16)
  aes = AES.new(key, AES.MODE_ECB, iv)
  data = aes.decrypt(data)
  return data.rstrip('\0')


def reply_plain(message):
  sys.stdout.write(message + '\n')


def reply_hex(message):
  # This is totally encrypted, right?
  sys.stdout.write(message.encode('hex') + '\n')


def main():
  global db
  reply = reply_plain

  datalen = struct.unpack('<I', sys.stdin.read(4))[0]
  data = ''
  while len(data) != datalen:
    s = sys.stdin.read(1)
    if not s:
      sys.exit(1)
    data += s
  data = decrypt(data)


  commands = data.split('\n')

  for cmd in commands:
    if not cmd:
      continue
    if ' ' in cmd:
      cmd, args = cmd.split(' ', 1)

    if cmd == 'HELLO':
      reply('WELCOME')
    elif cmd == 'SHOW':
      if args == 'VERSION':
        reply('NoRedisSQL v1.0')
      elif args == 'KEYS':
        reply(repr(db.keys()))
      elif args == 'ME THE MONEY':
        reply("Jerry, doesn't it make you feel good just to say that!")
      else:
        reply('u w0t m8')
    elif cmd == 'SET':
      key, value = args.split(' ', 1)
      db[key] = value
      reply('OK')
    elif cmd == 'GET':
      reply(args + ': ' + db.get(args, ''))
    elif cmd == 'SNIPPET':
      reply(db[args][:10] + '...')
    elif cmd == 'MD5':
      reply(md5(db.get(args, '')))
    elif cmd == 'ENCRYPTION':
      if args == 'HEX':
        reply = reply_hex
        reply('OK')
      elif args == 'OFF':
        reply = reply_plain
        reply('OK')
      else:
        reply('u w0t m8')
    else:
      reply('Unknown command %r' % (cmd))


if __name__ == '__main__':
  signal.alarm(10)
  signal.signal(signal.SIGALRM, lambda a,b: sys.exit(0))
  main()
