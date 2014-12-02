# Forensics-200: Obscurity


The third forensics problem starts with the following text:

> see or do not see
>
> Written by marc
>
> [pdf.pdf]
>


Hacking PDFs, what fun!  


In general, when dealing with reverse-engineering malicious documents, we follow these steps:
   1. We search for malicious embedded code (shell code, JavaScript).
   2. We extract any suspicious code segments
   3. If we see shell code, we disassemble or debug it. If we see JavaScript (or ActionScript or VB macro code), we try to examine it.

However, this problem turned out to be very simple...

---

## Finding the Flag in 10 Seconds

Yeap, this easy:

    1. Download the PDF file.
    2. Open it in any PDF viewer.
    3. CTRL+A (select all the contend).
    4. You see the flag!

![](http://i.imgur.com/b03EehK.png)

OK, we were luck. Keep reading if you think this was too easy.



## Analysing the ID and the Streams in a PDF File

Let's suppose we had no clue that the flag would just be a text in the file. In this case, we would want to examine the file's structure. For this task we use the [PDF Tool] suite, which is written in Python. 

#### pdfid

We start with *pdfid.py*, which parses the PDF  looking for certain  keywords. We download and unzip that script, and then we make it an executable:

```sh
$ unzip pdfid_v0_1_2.zip 
$ chmod a+x pdfid.py 
```

Running over our file gives:
```sh
$ ./pdfid.py pdf.pdf 
PDFiD 0.1.2 pdf.pdf
 PDF Header: %PDF-1.3
 obj                   20
 endobj                19
 stream                10
 endstream             10
 xref                   1
 trailer                1
 startxref              1
 /Page                  1
 /Encrypt               0
 /ObjStm                0
 /JS                    0
 /JavaScript            0
 /AA                    0
 /OpenAction            0
 /AcroForm              0
 /JBIG2Decode           0
 /RichMedia             0
 /Launch                0
 /EmbeddedFile          0
 /XFA                   0
 /Colors > 2^24         0
```

All right, no funny stuff going on here. We need to look deeper into each of the these streams.

#### pdf-parser

We download *pdf-parser.py*, which is used to search for all the fundamental elements in a PDF file. Let's take a closer look:

```sh
$ unzip pdf-parser_V0_4_3.zip
$ chmod a+x pdf-parser.py
$ ./pdf-parser.py 
Usage: pdf-parser.py [options] pdf-file|zip-file|url
pdf-parser, use it to parse a PDF document

Options:
  --version             show program's version number and exit
  -s SEARCH, --search=SEARCH
                        string to search in indirect objects (except streams)
  -f, --filter          pass stream object through filters (FlateDecode,
                        ASCIIHexDecode, ASCII85Decode, LZWDecode and
                        RunLengthDecode only)
  -o OBJECT, --object=OBJECT
                        id of indirect object to select (version independent)
  -r REFERENCE, --reference=REFERENCE
                        id of indirect object being referenced (version
                        independent)
  -e ELEMENTS, --elements=ELEMENTS
                        type of elements to select (cxtsi)
  -w, --raw             raw output for data and filters
  -a, --stats           display stats for pdf document
  -t TYPE, --type=TYPE  type of indirect object to select
  -v, --verbose         display malformed PDF elements
  -x EXTRACT, --extract=EXTRACT
                        filename to extract malformed content to
  -H, --hash            display hash of objects
  -n, --nocanonicalizedoutput
                        do not canonicalize the output
  -d DUMP, --dump=DUMP  filename to dump stream content to
  -D, --debug           display debug info
  -c, --content         display the content for objects without streams or
                        with streams without filters
  --searchstream=SEARCHSTREAM
                        string to search in streams
  --unfiltered          search in unfiltered streams
  --casesensitive       case sensitive search in streams
  --regex               use regex to search in streams
```

Very interesting! We run it with our file, searching for the string */ProcSet*:
```sh
$ ./pdf-parser.py  pdf.pdf | grep  /ProcSet
        /ProcSet [ /ImageC /Text /PDF /ImageI /ImageB ]
```
Awesome! Even though we don't see any text in the file (when we opened it in the PDF viewer), there is text somewhere!


## Getting Text from PDF


A good way to extract text from a pdf is using [pdftotext]:

```sh
$ pdftotext pdf.pdf
```

You should get a ```pdf.txt``` file. Reading it with Linux's commands ```cat``` or ```strings```gives you the flag:

```sh
$ strings pdf.txt 
flag{security_through_obscurity}	
```

As a note, there are several other PDF forensics tools that are worth to be mentioned: [Origami] (pdfextract extracts JavaScript from PDF files), [PDF Stream Dumper] (several PDF analysis tools), [Peepdf] (command-line shell for examining PDF), [PDF X-RAY Lite] (creates an HTML report with decoded file structure and contents), [SWF mastah] (extracts SWF objects), [Pyew](for examining and decoding structure and content of PDF files).





**Hack all the things!**
[PDF Tool]:http://blog.didierstevens.com/programs/pdf-tools/
[Origami]: http://esec-lab.sogeti.com/pages/Origami
[PDF Stream Dumper]: http://blog.zeltser.com/post/3235995383/pdf-stream-dumper-malicious-file-analysis
[Peepdf]: http://blog.zeltser.com/post/6780160077/peepdf-malicious-pdf-analysis
[SWF mastah]: http://blog.zeltser.com/post/12615013257/extracting-swf-from-pdf-using-swf-mastah
[PDF X-RAY Lite]: https://github.com/9b/pdfxray_lite
[Pyew]: http://code.google.com/p/pyew/wiki/PDFAnalysis

[this website]: http://blog.didierstevens.com/programs/pdf-tools/
[pdf-tools]: https://apps.fedoraproject.org/packages/pdf-tools
[pdf.pdf]: https://ctf.isis.poly.edu/static/uploads/883c7046854e04138c55680ffde90a61/pdf.pdf
[pdftotext]: http://en.wikipedia.org/wiki/Pdftotext