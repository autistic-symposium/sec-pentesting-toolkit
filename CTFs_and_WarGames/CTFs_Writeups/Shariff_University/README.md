# The Sharif University CTF 2014


## Avatar: Steganography

The challenge starts with:
> A terrorist has changed his picture in a social network. What is the hidden message?

And the following image:


![cyber](http://i.imgur.com/6NIu64us.jpg)



For this problem, I use [OutGuess], which can be installed as:

```sh
$ tar -zxvf outguess-0.2.tar.gz
$ cd outguess
$ ./configure && make
```
Running it will give us the flag:
```sh
$ ./outguess -r lamb.jpg pass.txt
Reading ../lamb.jpg....
Extracting usable bits:   28734 bits
Steg retrieve: seed: 94, len: 41
$ cat pass.txt
We should blow up the bridge at midnight
```

__________________________

## What is this: Steganography

This challenge has a very short text:

> Find the flag.

Together with two pictures:

![cyber](http://i.imgur.com/sbSwBju.jpg)
![cyber](http://i.imgur.com/mpcIKWt.jpg)

After the usual inspection (tail, file, diff, compare), I applied my knowledge of a former astrophysicist to inspect what would happen if I added or subtracted the picture. I wrote the following script:

```py
import sys

from scipy.misc import imread, imsave

def compare_images(img1, img2):
    diff = img1 + img2
    imsave('sum.png', diff)
    diff = img1 - img2
    imsave('diff.png', diff)

def main():
    file1, file2 = sys.argv[1:1+2]
    img1 = imread(file1).astype(float)
    img2 = imread(file2).astype(float)
    compare_images(img1, img2)

```

Running it, give us the flag!

![cyber](http://i.imgur.com/mvj8OJl.png)

--------------------
## Guess the number: Reverse Engineering

This problem starts with another not very informative text:
> Guess the number and find the flag.

Then it gives us a *java class* file. It was clear that we needed to decompile it. I'm using
[jad]for this task:

```sh
$ jad guess.class
```

Now, opening this file in a text editor, we can see how to generate the flag:
```java



```java
// Decompiled by Jad v1.5.8e. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.geocities.com/kpdus/jad.html
// Decompiler options: packimports(3)
// Source File Name:   guess.java

(...)
String str_one = "4b64ca12ace755516c178f72d05d7061";
 String str_two = "ecd44646cfe5994ebeb35bf922e25dba";
 String answer = XOR(str_one, str_two);
System.out.println((new StringBuilder("your flag is: ")).append(answer).toString());
```
Running the modified version gives us:
```java
$ javac -g guess.java
$ java guess
your flag is: a7b08c546302cc1fd2a4d48bf2bf2ddb
```

_________________
## Sudoku image encryption - cryptography

This challenge starts with the following text:
> Row Major Order

And it gives us two pictures: a map and a sudoku.

![cyber](http://i.imgur.com/U9Zq4wp.png)

We solve the sudoku and write the solution in a script to reorder the blocks:
```python
from PIL import Image


# solved sudoku
sudoku = '''
964127538
712385694
385496712
491578263
238614975
576239841
627843159
153962487
849751326
'''
s = sudoku.replace('\n', '')

image = Image.open('image.png').convert('RGB')
out = Image.new('RGB', image.size)

for j in range(9):
    for i in range(9):
      img_cell = image.crop((i * 50, j * 50, i * 50 + 50, j * 50 + 50))
      c = (int(s[j * 9 + i]) - 1) * 50
      out.paste(img_cell, (c, j * 50))

out.save('out_image.png')
```

This gives us our flag:

![cyber](http://i.imgur.com/sA7JPrl.png)


** Hack all the things! **


[OutGuess]: http://www.outguess.org/download.php
[jad]:  http://varaneckas.com/jad/

