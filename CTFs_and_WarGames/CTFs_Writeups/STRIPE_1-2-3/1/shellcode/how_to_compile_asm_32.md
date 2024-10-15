as --32 -o s.o   s.s  
ld -m elf_i386 -o s s.o 
./s
objdump -d s

