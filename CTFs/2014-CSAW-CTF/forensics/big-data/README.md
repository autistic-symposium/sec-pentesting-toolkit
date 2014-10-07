# Forensics-100: dumpster diving

This is the first forensic problem, and it is only 100 points. The problem starts with the following text:

> dumpsters are cool, but cores are cooler
>
> Written by marc
>
> [firefox.mem.zip]



----------

##Unziping firefox.mem.zip 

The given file has a funny extension *.mem.zip*. Before we go ahead and unzip it, let's try to learn more about this file. To do this we choose to use the Linux's command [file]:

```sh
$ file --help
Usage: file [OPTION...] [FILE...]
Determine type of FILEs.

      --help                 display this help and exit
  -v, --version              output version information and exit
  -m, --magic-file LIST      use LIST as a colon-separated list of magic
                               number files
  -z, --uncompress           try to look inside compressed files
  -b, --brief                do not prepend filenames to output lines
  -c, --checking-printout    print the parsed form of the magic file, use in
                               conjunction with -m to debug a new magic file
                               before installing it
  -e, --exclude TEST         exclude TEST from the list of test to be
                               performed for file. Valid tests are:
                               apptype, ascii, cdf, compress, elf, encoding,
                               soft, tar, text, tokens
  -f, --files-from FILE      read the filenames to be examined from FILE
  -F, --separator STRING     use string as separator instead of `:'
  -i, --mime                 output MIME type strings (--mime-type and
                               --mime-encoding)
      --apple                output the Apple CREATOR/TYPE
      --mime-type            output the MIME type
      --mime-encoding        output the MIME encoding
  -k, --keep-going           don't stop at the first match
  -l, --list                 list magic strength
  -L, --dereference          follow symlinks (default)
  -h, --no-dereference       don't follow symlinks
  -n, --no-buffer            do not buffer output
  -N, --no-pad               do not pad output
  -0, --print0               terminate filenames with ASCII NUL
  -p, --preserve-date        preserve access times on files
  -r, --raw                  don't translate unprintable chars to \ooo
  -s, --special-files        treat special (block/char devices) files as
                             ordinary ones
  -C, --compile              compile file specified by -m
  -d, --debug                print debugging messages
```

We find the flag ```-z```, which allows us to look inside the zipped files:

```sh
$  file -z firefox.mem.zip 
firefox.mem.zip: ELF 64-bit LSB core file x86-64, version 1 (SYSV) (Zip archive data, at least v2.0 to extract)
```
Cool! So let's go ahead and unzip this file:

```sh
$ unzip firefox.mem.zip nzip firefox.mem.zip
Archive:  firefox.mem.zip
  inflating: firefox.mem             
   creating: __MACOSX/
  inflating: __MACOSX/._firefox.mem 
```

--------



## Extra: Learning More about the *.mem* File

This is a very weird file extension. If you google *.mem*, you don't find much, it's clear it's a memory file, but what now?  From the *file* command, we learned that this is an *ELF 64-bit LSB core*. Let's understand this  by parts. 

An [ELF] file  (Executable and Linkable Format) is a standard file format for executables, object code, shared libraries, and core dumps. The cool thing about ELF is that it's not bound to any particular architecture. 

In Linux, we can use the command [readelf] to displays information about ELF files:


```sh
$ readelf firefox.mem
Usage: readelf <option(s)> elf-file(s)
 Display information about the contents of ELF format files
 Options are:
  -a --all               Equivalent to: -h -l -S -s -r -d -V -A -I
  -h --file-header       Display the ELF file header
  -l --program-headers   Display the program headers
     --segments          An alias for --program-headers
  -S --section-headers   Display the sections' header
     --sections          An alias for --section-headers
  -g --section-groups    Display the section groups
  -t --section-details   Display the section details
  -e --headers           Equivalent to: -h -l -S
  -s --syms              Display the symbol table
     --symbols           An alias for --syms
  --dyn-syms             Display the dynamic symbol table
  -n --notes             Display the core notes (if present)
  -r --relocs            Display the relocations (if present)
  -u --unwind            Display the unwind info (if present)
  -d --dynamic           Display the dynamic section (if present)
  -V --version-info      Display the version sections (if present)
  -A --arch-specific     Display architecture specific information (if any)
  -c --archive-index     Display the symbol/file index in an archive
  -D --use-dynamic       Use the dynamic section info when displaying symbols
  -x --hex-dump=<number|name>
                         Dump the contents of section <number|name> as bytes
  -p --string-dump=<number|name>
                         Dump the contents of section <number|name> as strings
  -R --relocated-dump=<number|name>
                         Dump the contents of section <number|name> as relocated bytes
  -w[lLiaprmfFsoRt] or
  --debug-dump[=rawline,=decodedline,=info,=abbrev,=pubnames,=aranges,=macro,=frames,
               =frames-interp,=str,=loc,=Ranges,=pubtypes,
               =gdb_index,=trace_info,=trace_abbrev,=trace_aranges]
                         Display the contents of DWARF2 debug sections
  --dwarf-depth=N        Do not display DIEs at depth N or greater
  --dwarf-start=N        Display DIEs starting with N, at the same depth
                         or deeper
  -I --histogram         Display histogram of bucket list lengths
  -W --wide              Allow output width to exceed 80 characters
  @<file>                Read options from <file>
  -H --help              Display this information
  -v --version           Display the version number of readelf

```


In addition, [LSB] stands for *Linux Standard Base*, which is a joint project by several Linux distributions. It specifies standard libraries, a number of commands and utilities that extend the POSIX standard, the layout of the file system hierarchy, run levels, the printing system, etc.




---

## Extracting Information from the *.mem* File

It turned out that we don't even need to know anything about the file to find the flag. All we need to do is to search for the *flag* string:

```sh
$ cat firefox.mem | grep -a 'flag{'
P��negativeone_or_fdZZZZZZZZZZZZnegativeone_or_nothingZZnegativeone_or_ssize_tZZd_name_extra_sizeZZZZZZZZZZZZnull_or_dirent_ptrZZZZZZZZZZOSFILE_SIZEOF_DIRZZZZZZZZZZZZ���� 3���������ZZZZZZZH�f�L��L��ZZ����@�m���������ZZZZZZZAG�@r���y��ZZZZZZZZflag{cd69b4957f06cd818d7bf3d61980e291}
```

Yay! We found the flag: **cd69b4957f06cd818d7bf3d61980e291**!

**Hack all the things!**


[LSB]: http://en.wikipedia.org/wiki/Linux_Standard_Base
[readelf]: http://linux.die.net/man/1/readelf
[file]: http://en.wikipedia.org/wiki/File_(command)
[firefox.mem.zip]: https://ctf.isis.poly.edu/static/uploads/606580b079e73e14ab2751e35d22ad44/firefox.mem.zip
[ELF]: http://en.wikipedia.org/wiki/Executable_and_Linkable_Format