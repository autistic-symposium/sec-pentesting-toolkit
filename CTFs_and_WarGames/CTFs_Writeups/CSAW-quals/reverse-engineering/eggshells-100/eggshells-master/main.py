# try:
#     from distorm import *
#     module = 'distorm'
# except ImportError:
import utils
try:
    from nasm import *
    module = 'nasm'
except ImportError:
    raise EnvironmentError("Couldn't find distorm or nasm")

from Tkinter import *
from ttk import *

import codecs
import subprocess
import sys
import interpreter
import sqlite3

class Disassembler():
    def __init__(self, frame):

        top = Frame(frame)
        self.shell_bar = Scrollbar(top)
        self.shell_bar.pack(side=RIGHT, fill=Y, expand=0)
        self.shellcode = Text(top, yscrollcommand=self.shell_bar.set)
        self.shellcode.pack(anchor=W, fill=BOTH, expand=1)
        self.shellcode.config(height=4, bd=2)
        self.shell_bar.config(command=self.shellcode.yview)

        bottom = Frame(frame)
        self.disasm_bar = Scrollbar(bottom)
        self.disasm_bar.pack(side=RIGHT, fill=Y, expand=0)
        self.disasm = Text(bottom, yscrollcommand=self.disasm_bar.set)
        self.disasm.pack(anchor=W, fill=BOTH, expand=1)
        self.disasm.config(height=4, bd=2)
        self.shell_bar.config(command=self.disasm.yview)

        top.pack(anchor=W, fill=BOTH, expand=1)
        bottom.pack(anchor=W, fill=BOTH, expand=1)

        var = IntVar()

        R1 = Radiobutton(frame, text="16-bit", variable=var, value=1, command=lambda: self.value(16))
        R1.pack(side=LEFT)

        R2 = Radiobutton(frame, text="32-bit", variable=var, value=2, command=lambda: self.value(32))
        R2.pack(side=LEFT)

        R3 = Radiobutton(frame, text="64-bit", variable=var, value=3, command=lambda: self.value(64))
        R3.pack(side=LEFT)

        B = Button(frame, text="Disassemble", command=self.render)
        B.pack(side=RIGHT)

    def value(self, val):
        '''
        Sets disassembler mode (e.g. 16bit, 32bit, or 64bit)
        '''
        global mode
        self.mode = val

    def clean(self, shellcode):
        '''
        Cleans the format that we get from tkinter into a format we can disassemble easily. (i.e. \x00\x00)
        '''
        return codecs.escape_decode(shellcode.decode('utf-8').strip())[0]

    def render(self):
        '''
        Cleans out the Text widget, does the disassembly and inserts it.
        '''
        self.disasm.delete(1.0, END)
        self.disasm.insert(INSERT, disassemble(self.clean(self.shellcode.get(1.0, END)), self.mode))

class Assembler():
    def __init__(self, frame):
        self.assembler = Text(frame)
        self.assembler.pack(fill=BOTH, expand=1)
        self.assembler.config(height=8, bd=2)

        self.output = Text(frame)
        self.output.pack(anchor=W, fill=BOTH, expand=1)
        self.output.config(height=4, bd=2)

        self.value = StringVar()
        self.dropdown = Combobox(frame, textvariable=self.value, state='readonly')
        self.dropdown['values'] = ('elf', 'elf64', 'bin')
        self.dropdown.current(0)
        self.dropdown.pack(side=LEFT)

        self.asm_button = Button(frame, text="Assemble", command=self.render)
        self.asm_button.pack(side=RIGHT)

        self.asm_test = Button(frame, text="Test Shellcode", command=self.test)
        self.asm_test.pack(side=RIGHT)

    def render(self):
        mode = self.dropdown['values'][self.dropdown.current()]
        asm = str(self.assembler.get(1.0, END))
        self.output.delete(1.0, END)
        self.output.insert(INSERT, repr(assemble(asm, mode))[1:-1] )

    def clean(self, shellcode):
        '''
        Cleans the format that we get from tkinter into a format we can disassemble easily. (i.e. \x00\x00)
        '''
        return codecs.escape_decode(shellcode.decode('utf-8').strip())[0]

    def test(self):
        shellcode = repr(self.clean(self.output.get(1.0, END)))[1:-1]
        subprocess.Popen([sys.executable, 'shellcode.py', shellcode]).communicate()

    def draw(self):
    	pass

class Shellcode():
    def __init__(self, frame):
        tree = Treeview(frame)

        # Inserted at the root, program chooses id:
        tree.insert('', 'end', 'windows', text='Windows')
        tree.insert('', 'end', 'linux', text='Linux')
         
        # Same thing, but inserted as first child:
        # tree.insert('', 0, 'gallery', text='Applications')

        # Treeview chooses the id:


        # Inserted underneath an existing node:
        tree.insert('windows', 'end', text='Canvas')
        tree.insert('linux', 'end', text='Canvas')

        tree.pack(side=LEFT, fill=Y)

class ConnectBack():
    def __init__(self, frame):
        pass


root = Tk()
root.title("Eggshells - " + module)
note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
tab4 = Frame(note)
tab5 = Frame(note)
tab6 = Frame(note)

#################DISASM################
Disassembler(tab1)
#######################################

################ASM####################
Assembler(tab2)
#######################################

###############Shellcode###############
Shellcode(tab6)
#######################################


################Python#################
c = interpreter.Console(tab4)
c.dict["console"] = c
c.pack(fill=BOTH, expand=1)
#######################################

note.add(tab1, text = "Disassembler")
note.add(tab2, text = "Assembler")
note.add(tab3, text = "Sockets")
note.add(tab4, text = "Python")
note.add(tab5, text = "Hex Editor")
note.add(tab6, text = "Shellcode")

note.pack(fill=BOTH, expand=1)
root.mainloop()
exit()