import utils
from capstone import *

def arch(arch):
    if arch == 'arm':
        return CS_ARCH_ARM
    elif arch == 'arm64':
        return CS_ARCH_ARM64
    elif arch == 'mips':
        return CS_ARCH_MIPS
    elif arch == 'x86':
        return CS_ARCH_X86


def mode(mode):
    if mode == 'arm':
        return CS_MODE_ARM
    elif mode == 'thumb':
        return CS_MODE_THUMB
    elif mode == '16' or mode == 16:
        return CS_MODE_16
    elif mode == '32' or mode == 32:
        return CS_MODE_32
    elif mode == '64' or mode == 64:
        return CS_MODE_32


def disassemble(code, _arch, _mode):
    _arch = arch(_arch)
    _mode = mode(_mode)

    md = Cs(_arch, _mode)

    disassembly = []

    for i in md.disasm(CODE, 0x0000000):
        disassembly.append(
            (i.address, len(str(i.bytes).encode('hex')) / 2, str(i.bytes).encode('hex'), i.mnemonic, i.op_str))

    return disassembly


CODE = "\x90\x90\x90"

for x in disassemble(CODE, 'x86', '64'):
    print "0x%08x (%02x) %-20s %s %s" % (x[0], x[1], x[2], x[3], x[4])
