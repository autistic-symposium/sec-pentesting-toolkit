# Gray Hacker Resources 

For fun or profit.


## Resource in this Repository

* [CTFs and WARGAMES](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/CTFs_and_WarGames)
* [CRYPTOGRAPHY](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Cryptography)
* [FORENSICS](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Forensics)
* [LINUX HACKING](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Linux_Hacking)
* [MEMORY EXPLOITS](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Memory_Exploits)
* [VULNERABILITIES AND EXPLOITS](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Vulnerabilities_and_Exploits)
* [NETWORK and 802.11](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Network_and_802.11)
* [REVERSE ENGINEERING](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Reverse_Engineering)
* [RUBBER DUCK](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Rubber_Duck)
* [STEGANOGRAPHY](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Steganography)
* [WEB EXPLOITS](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Web_Security)
* [OTHER HACKINGS](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Other_Hackings)
* [PEN TESTING](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Pen_Testing)
* [MOBILE](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Mobile)
* [BOTNETS](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Botnets)
* [DDOS](https://github.com/bt3gl/Gray_Hacking_Toolkit/tree/master/Ddos)

----

### Post-Exploitation

* [Metasploit Post Exploitation Command List](https://docs.google.com/document/d/1ZrDJMQkrp_YbU_9Ni9wMNF2m3nIPEA_kekqqqA2Ywto/edit)
* [Obscure Systems (AIX, Embeded, etc) Post-Exploit Command List](https://docs.google.com/document/d/1CIs6O1kMR-bXAT80U6Jficsqm0yR5dKUfUQgwiIKzgc/edit).
* [OSX Post-Exploitation](https://docs.google.com/document/d/10AUm_zUdAQGgoHNo_eS0SO1K-24VVYnulUD2x3rJD3k/edit?hl=en_US).
* [Windows Post-Exploitation Command List](https://docs.google.com/document/d/1U10isynOpQtrIK6ChuReu-K1WHTJm4fgG3joiuz43rw/edit?hl=en_US).
* [Linux/Unix/BSD Post-Exploitation Command List](https://docs.google.com/document/d/1ObQB6hmVvRPCgPTRZM5NMH034VDM-1N-EWPRz2770K4/edit?hl=en_US).

----

### Useful CLI

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


#### Security analyzers and scanners for CI/CD pipelines

* Static code security analyzers: [SonarQube](https://www.sonarqube.org/) (Javascript scanner), [NodeJsScan](https://github.com/ajinabraham/NodeJsScan).
* Package dependency security analyzers: [Snyk](https://snyk.io/)
* Docker image security analyzers: [Hadolint](https://github.com/hadolint/hadolint), [Clair](https://github.com/coreos/clair), [Anchore](https://anchore.com/)
* AWS IAM permission analyzers: [IAM access advisor APIs](https://aws.amazon.com/blogs/security/automate-analyzing-permissions-using-iam-access-advisor/), [PMapper](https://github.com/nccgroup/PMapper).
* AWS S3 permission analyzers: [s3audit](https://github.com/scalefactory/s3audit).
* Docker runtime anomaly detection: [Falco](https://hub.docker.com/r/sysdig/falco).
* Kubernetes policy security analyzers: [RBAC](https://searchsecurity.techtarget.com/definition/role-based-access-control-RBAC). 
* Policy auditing tools: [Rakkess](https://github.com/corneliusweig/rakkess).


### Books

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
- [Shellcoders Handbook](http://www.amazon.com/The-Shellcoders-Handbook-Discovering-Exploiting/dp/047008023X)
- [Practice Malware Analysis](https://www.nostarch.com/malware)



#### Articles:
* [Continuous security](https://www.infoq.com/news/2019/08/continuous-security/).
* [How to not get hacked](https://kubernetes.io/blog/2018/07/18/11-ways-not-to-get-hacked/).


#### Fun

- [Spam Nation](http://www.amazon.com/Spam-Nation-Organized-Cybercrime-Epidemic/dp/1492603236/ref=tmm_pap_swatch_0?_encoding=UTF8&sr=&qid=)
- [The Art of Intrusion](http://www.amazon.com/The-Art-Intrusion-Intruders-Deceivers/dp/0471782661http://www.amazon.com/The-Art-Intrusion-Intruders-Deceivers/dp/0471782661)
- [This Machine Kills Secrets](http://www.amazon.com/This-Machine-Kills-Secrets-Whistleblowers/dp/0142180491/ref=sr_1_1?s=books&ie=UTF8&qid=1436039456&sr=1-1&keywords=this+Machine+Kills+Secrets)

### Other Resources

- Krebs Series on how to be in InfoSec: [Thomas Ptacek](http://krebsonsecurity.com/2012/06/how-to-break-into-security-ptacek-edition/#more-15594), [Bruce Schneier](http://krebsonsecurity.com/2012/07/how-to-break-into-security-schneier-edition/#more-15592), [Charlie Miller](http://krebsonsecurity.com/category/how-to-break-into-security/)
- [How to be a InfoSec Geek](http://www.primalsecurity.net/how-to-be-an-infosec-geek/)
- [My Blog](http://bt3gl.github.io/index.html)

