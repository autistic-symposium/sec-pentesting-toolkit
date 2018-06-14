# Gray Hacker Resources

A big bag of Fun. Educational purposes.

[url=https://ibb.co/dirtjd][img]https://preview.ibb.co/eO9PqJ/DJI_0062.jpg[/img][/url]


##

### * [CTFs and WARGAMES](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/CTFs_and_WarGames)
### * [CRYPTOGRAPHY](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Cryptography)
### * [FORENSICS](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Forensics)
### * [LINUX HACKING](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Linux_Hacking)
### * [MEMORY EXPLOITS](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Memory_Exploits)
### * [VULNERABILITIES AND EXPLOITS](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Vulnerabilities_and_Exploits)
### * [NETWORK and 802.11](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Network_and_802.11)
### * [REVERSE ENGINEERING](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Reverse_Engineering)
### * [RUBBER DUCK](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Rubber_Duck)
### * [STEGANOGRAPHY](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Steganography)
### * [WEB EXPLOITS](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Web_Security)
### * [OTHER HACKINGS](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Other_Hackings)
### * [PEN TESTING](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Pen_Testing)
### * [MOBILE](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Mobile)
### * [BOTNETS](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Botnets)

----

### Post-Exploitation

* [Metasploit Post Exploitation Command List](https://docs.google.com/document/d/1ZrDJMQkrp_YbU_9Ni9wMNF2m3nIPEA_kekqqqA2Ywto/edit)

* [Obscure Systems (AIX, Embeded, etc) Post-Exploit Command List](https://docs.google.com/document/d/1CIs6O1kMR-bXAT80U6Jficsqm0yR5dKUfUQgwiIKzgc/edit).

* [OSX Post-Exploitation](https://docs.google.com/document/d/10AUm_zUdAQGgoHNo_eS0SO1K-24VVYnulUD2x3rJD3k/edit?hl=en_US).

* [Windows Post-Exploitation Command List](https://docs.google.com/document/d/1U10isynOpQtrIK6ChuReu-K1WHTJm4fgG3joiuz43rw/edit?hl=en_US).

* [Linux/Unix/BSD Post-Exploitation Command List](https://docs.google.com/document/d/1ObQB6hmVvRPCgPTRZM5NMH034VDM-1N-EWPRz2770K4/edit?hl=en_US).

----

### Useful Command Line

#### Searching


```
grep word f1

sort | uniq -c

diff f1 f2

find -size f1
```




#### Compressed Files


```
zcat f1 > f2

gzip -d file

bzip2 -d f1

tar -xvf file
```



#### Connecting to a Server/Port

```

nc localhost 30000

echo 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e | nc localhost 30000

openssl s_client -connect localhost:30001 -quiet

nmap -p 31000-32000 localhost

telnet localhost 3000
```


----

## References:

### Books I Recommend

#### Technical
- [Bulletproof SSL and TLS](http://www.amazon.com/gp/product/1907117040?psc=1&redirect=true&ref_=oh_aui_detailpage_o06_s00)
- [Reversing: Secrets of Reverse Engineering](http://www.amazon.com/Reversing-Secrets-Engineering-Eldad-Eilam/dp/0764574817)
- [The Art of Memory Forensics](http://www.amazon.com/gp/product/1118825098?psc=1&redirect=true&ref_=oh_aui_search_detailpage)
- [The C Programming Language](http://www.amazon.com/gp/product/0131103628?psc=1&redirect=true&ref_=oh_aui_search_detailpage)
- [The Unix Programming Environment](http://www.amazon.com/gp/product/013937681X?psc=1&redirect=true&ref_=oh_aui_search_detailpage)
- [UNIX Network Programming](http://www.amazon.com/gp/product/0139498761?psc=1&redirect=true&ref_=oh_aui_search_detailpage)
- [Threat Modeling: Designing for Security](http://www.amazon.com/Threat-Modeling-Designing-Adam-Shostack/dp/1118809998)
- [The Tangled Web](http://www.amazon.com/The-Tangled-Web-Securing-Applications/dp/1593273886)
- [The Art of Exploitation](http://www.amazon.com/Hacking-The-Art-Exploitation-Edition/dp/1593271441)
- [The Art of Software Security Assessment](http://www.amazon.com/The-Software-Security-Assessment-Vulnerabilities/dp/0321444426)
- [Practical Packet Analysis](http://www.nostarch.com/packet2.htm)
- [Gray Hat Python](http://www.amazon.com/Gray-Hat-Python-Programming-Engineers/dp/1593271921)
- [Black Hat Python](http://www.nostarch.com/blackhatpython)
- [Violent Python](http://www.amazon.com/Violent-Python-Cookbook-Penetration-Engineers/dp/1597499579)
- [Shellcoders Handbook](www.amazon.com/The-Shellcoders-Handbook-Discovering-Exploiting/dp/047008023X)
- [Practice Malware Analysis](https://www.nostarch.com/malware)

#### Fun

- [Spam Nation](http://www.amazon.com/Spam-Nation-Organized-Cybercrime-Epidemic/dp/1492603236/ref=tmm_pap_swatch_0?_encoding=UTF8&sr=&qid=)
- [The Art of Intrusion](http://www.amazon.com/The-Art-Intrusion-Intruders-Deceivers/dp/0471782661http://www.amazon.com/The-Art-Intrusion-Intruders-Deceivers/dp/0471782661)
- [This Machine Kills Secrets](http://www.amazon.com/This-Machine-Kills-Secrets-Whistleblowers/dp/0142180491/ref=sr_1_1?s=books&ie=UTF8&qid=1436039456&sr=1-1&keywords=this+Machine+Kills+Secrets)

### Other Resources

- Krebs Series on how to be in InfoSec: [Thomas Ptacek](http://krebsonsecurity.com/2012/06/how-to-break-into-security-ptacek-edition/#more-15594), [Bruce Schneier](http://krebsonsecurity.com/2012/07/how-to-break-into-security-schneier-edition/#more-15592), [Charlie Miller](http://krebsonsecurity.com/category/how-to-break-into-security/)
- [How to be a InfoSec Geek](http://www.primalsecurity.net/how-to-be-an-infosec-geek/)
- [My Blog](http://bt3gl.github.io/index.html)


----

### License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/)


