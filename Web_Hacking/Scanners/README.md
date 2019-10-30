## [Nikto](http://sectools.org/tool/nikto/)

* Nikto is an Open Source (GPL) web server scanner which performs comprehensive tests against web servers for multiple items, including over 6400 potentially dangerous files/CGIs, checks for outdated versions of over 1200 servers, and version specific problems on over 270 servers. It also checks for server configuration items such as the presence of multiple index files, HTTP server options, and will attempt to identify installed web servers and software.

* Most scanned vulnerabilities are things such as XSS, phpmyadmin logins,
etc.


* It's coded in Perl.

* It is not a stealthy tool. It will test a web server in the quickest time possible, and it is  obvious in log files.

* There is support for LibWhisker's anti-IDS methods.

* To fire it up in a website:

```
$ ./nikto.pl -h <IP> -p <PORT> -output <OUTPUT-FILE>
```

* The output file can be open with *Niktorat*.


## [W3af](http://w3af.org/)

* w3af is a Web Application Attack and Audit Framework. The project's goal is to create a framework to help you secure your web applications by finding and exploiting all web application vulnerabilities.

* It's coded in Python.

* It has plugins that communicate with each other.

* It removes some of the headaches involved in manual web application testing through its Fuzzy and manual request generator feature.

* It can be configured to run as a MITM proxy. The requests intercepted can be sent to the request generator and then manual web application testing can be peperformedsing variables parameters.

* It also has features to exploit the vulnerabilities that it finds. w3af supports detection of both simple and blind  OS commanding vulnerability.

