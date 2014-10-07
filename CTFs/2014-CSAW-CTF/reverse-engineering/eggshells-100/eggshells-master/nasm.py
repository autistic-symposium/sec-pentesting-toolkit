import utils
import os
import subprocess
import tempfile
import sys
import re

subprocess.STARTF_USESHOWWINDOW = 1 # Hiding console windows in subprocess calls

if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    NASM = '/usr/bin/nasm'
    NDISASM = '/usr/bin/ndisasm'

elif sys.platform.startswith('win32'):
    NASM = 'nasm/nasm.exe'
    NDISASM = 'nasm/ndisasm.exe'

if not os.path.exists(NASM):
    raise EnvironmentError('nasm not found')
if not os.path.exists(NDISASM):
    raise EnvironmentError('ndisasm not found')

hex_regex = re.compile(r'0x\w*')

def delete_file(filename):
    """
    Deletes file from the disk if it exists
    """
    if os.path.exists(filename):
        os.unlink(filename)


def assemble(asm, mode="elf"):
    '''
    Assemble using nasm, return raw hex bytes.
    '''
    temp = tempfile.NamedTemporaryFile(delete=False)

    linkme = tempfile.NamedTemporaryFile(delete=False)
    dir = tempfile.gettempdir()
    try:
        temp.write(asm)
        temp.close()
        linkme.close()

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        
        link = subprocess.check_output([NASM, '-f ' + mode, temp.name, '-o ' + dir + '/link.o'], startupinfo=startupinfo)
        out = subprocess.check_output([NASM, temp.name, '-o ' + temp.name + '.elf'], startupinfo=startupinfo)

        asm = open(temp.name + '.elf', 'rb')
        asm = asm.read()
        delete_file(temp.name + '.elf')
        delete_file(linkme.name)
        delete_file(dir + '/link.o')
        delete_file(temp.name)
        return asm
    except:
        delete_file(temp.name + '.elf')
        delete_file(linkme.name)
        delete_file(dir + '/link.o')
        delete_file(temp.name)
        return "assembly failed"


def disassemble(elf, mode=32):
    '''
    Disassemble using ndisasm. Return the output.
    '''
    temp = tempfile.NamedTemporaryFile(delete=False)
    try:
        temp.write(elf)
        temp.close()

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW

        asm = subprocess.check_output([NDISASM, '-a', '-b ' + str(mode), temp.name], startupinfo=startupinfo)
        delete_file(temp.name)

    except:
        delete_file(temp.name)
        return 'disassembly failed'

        #return asm
        
    disasm = asm.split('\n')
    disasm = [" ".join(x.split()).split(' ', 2) for x in disasm ]

    # Join line continuations together and mark them for removal
    marked = []
    for x in range(len(disasm)):
        if len(disasm[x]) == 1:
            disasm[x-1][1] += disasm[x][0][1:]
            marked.append(x)
    for x in marked[::-1]:
        disasm.pop(x)        

    # Join the disassembly back together for output
    # Also provide string and decimal representations of hex values
    disassembly = ''
    for line in disasm:
        hexvals = hex_regex.findall(line[2])
        if len(hexvals) > 0 and ('push' in line[2] or 'mov' in line[2]):
            line = list(line) # Why you give me tuple Distorm?
            if len(hexvals[0][2:]) > 2:
                line[2] = line[2] + '\t; ' + hexvals[0][2:].decode('hex')
            else:
                line[2] = line[2] + '\t; ' + str(int(hexvals[0], 16))

        disassembly += "0x%08s (%02x) %-20s %s" % (line[0], len(line[1])//2, line[1], line[2]) + "\n"
    return disassembly


if __name__ == '__main__':
    print disassemble('\x48\x31\xc0\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\xb0\x3b\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x0f\x05', 64)

    asm = '''
    BITS 32
    main:
            ; execve("/bin/sh", 0, 0)
            xor eax, eax
            push eax
            push 0x68732f2f         ; "//sh" -> stack
            push 0x6e69622f         ; "/bin" -> stack
            mov ebx, esp                ; arg1 = "/bin//sh\0"
            mov ecx, eax                ; arg2 = 0
            mov edx, eax                ; arg3 = 0
            mov al, 11
            int 0x80
    '''
    print repr(assemble(asm, "elf"))
