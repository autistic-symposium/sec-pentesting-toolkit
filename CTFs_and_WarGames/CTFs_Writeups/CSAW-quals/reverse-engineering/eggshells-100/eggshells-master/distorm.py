import utils
import distorm3
import re

hex_regex = re.compile(r'0x\w*')

def disassemble(shellcode, mode=32):
    '''
    Does disassembly with distorm3 and handles the string joining
    '''
    if mode == 32:
        disasm = distorm3.Decode(0x0, shellcode, distorm3.Decode32Bits)

    elif mode == 64:
        disasm = distorm3.Decode(0x0, shellcode, distorm3.Decode64Bits)

    elif mode == 16:
        disasm = distorm3.Decode(0x0, shellcode, distorm3.Decode16Bits)

    disassembly = ''
    for line in disasm:

        hexvals = hex_regex.findall(line[2])
        if len(hexvals) > 0 and ('PUSH' in line[2] or 'MOV' in line[2]):
            line = list(line) # Why you give me tuple Distorm?
            if len(hexvals[0][2:]) > 2:
                line[2] = line[2] + '\t; ' + hexvals[0][2:].decode('hex')
            else:
                line[2] = line[2] + '\t; ' + str(int(hexvals[0], 16))

        disassembly += "0x%08x (%02x) %-20s %s" % (line[0], line[1], line[3], line[2]) + "\n"

    return disassembly

if __name__ == '__main__':
    print disassemble('\x48\x31\xc0\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\xb0\x3b\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x0f\x05', 64)
