# Hacking the Web with Python's urllib2 (by bt3)

Python's  [urllib2](https://docs.python.org/2/library/urllib2.html) library is **the tool** to interact with web services, with several functions and classes to help handling URLs. **urllib2** is written in the top of [httplib](https://docs.python.org/2/library/httplib.html) library (which defines classes to implement the client side of HTTP and HTTPs). In turn, **httplib** uses the [socket](http://bt3gl.github.io/black-hat-python-networking-the-socket-module.html) library.

In this post I [introduce urllib2](#intro) and then I work on two problems: [mapping  webapps  from their installation files](#map) and [brute-forcing the contents of webapps to find hidden resources](#brute1).


-----

## <a name="intro"></a>urllib2 101


The easiest way to start is by taking a look at the **urlopen** method, which returns an object similar to a **file** in Python (plus three more methods: **geturl**, for the URL of the resource; **info**, for meta-information; and **getcode**, for HTTP status code).



### A Simple GET
Let's see how a simple [GET](http://www.w3schools.com/tags/ref_httpmethods.asp) request works. This is done directly  with [urlopen](https://docs.python.org/2/library/urllib2.html#urllib2.urlopen):


```python
>>> import urllib2
>>> msg = urllib2.urlopen('http://www.google.com')
>>> print msg.read(100)
<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="en"><head><meta content="Search the world's information, including (...)
```

Notice that, differently from modules such as [scapy](http://bt3gl.github.io/black-hat-python-infinite-possibilities-with-the-scapy-module.html) or [socket](http://bt3gl.github.io/black-hat-python-the-socket-module.html), we *need to specify the protocol* in the URL (HTTP).

Now, let's be fancy and customize the output:

```python
import urllib2

response = urllib2.urlopen('http://localhost:8080/')
print 'RESPONSE:', response
print 'URL     :', response.geturl()

headers = response.info()
print 'DATE    :', headers['date']
print 'HEADERS :'
print headers

data = response.read()
print 'LENGTH  :', len(data)
print 'DATA    :'
print data
```

Which leads to something like this:
```sh
RESPONSE: <addinfourl at 140210027950304 whose fp = <socket._fileobject object at 0x7f8530eec350>>
URL     : http://www.google.com
DATE    : Tue, 23 Dec 2014 15:04:32 GMT
HEADERS :
Date: Tue, 23 Dec 2014 15:04:32 GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=ISO-8859-1
Set-Cookie: PREF=ID=365306c56a0ffee1:FF=0:TM=1419951872:LM=1419951872:S=lyvP_3cexMCllrVl; expires=Thu, 22-Dec-2016 15:04:32 GMT; path=/; domain=.google.com
Set-Cookie: NID=67=fkMfihQT2bLXyqQ8PIge1TwighxcsI4XVUWQl-7KoqW5i3T-jrzUqrC_lrtO7zd0vph3AzSMxwz2LkdWFN479RREL94s0hqRq3kOroGsUO_tFzBhN1oR9bDRMnW3hqOx; expires=Wed, 01-Jul-2015 15:04:32 GMT; path=/; domain=.google.com; HttpOnly
Server: gws
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Alternate-Protocol: 80:quic,p=0.02
Connection: close

LENGTH  : 17393
DATA    :
<!doctype html>(...)
```


### A simple POST

[POST](http://www.w3schools.com/tags/ref_httpmethods.asp) requests send data to a URL ([often refering](https://docs.python.org/2/howto/urllib2.html#data) to [CGI](http://en.wikipedia.org/wiki/Common_Gateway_Interface) scripts or forms in a web applications).

POST requests, differently from GET requests, usually have side-effects such as changing the state of the system. But data can also be passed in an HTTP GET reqest by encoding it in the URL.

In the case of a HTTML form, the data needs to be encoded and  this encoding is made with [urllib](https://docs.python.org/2/library/urllib.html)'s method **urlencode** (a method used for the generation
of GET query strings):


```python
import urllib
import urllib2

data = { 'q':'query string', 'foo':'bar' }
encoded_data = urllib.urlencode(data)

url = 'http://localhost:8080/?' + encoded_data

response = urllib2.urlopen(url)
print response.read()
```

In reality, when working with **urllib2**, a more efficient way to customize the **urlopen** method is by passing a **Request object** as the data argument:

```python
data = { 'q':'query string', 'foo':'bar' }
encoded_data = urllib.urlencode(data)

req = urllib2.Request(url, encoded_data)

response = urllib2.urlopen(req)
print response.read()
```

That's one of the differences between **urllib2** and **urllib**: the former can accept a **Request object** to set the headers for a URL request, while the last  accepts only a URL.



### Headers

As we have learned above, we can create a GET request using not only strings but also the [Request](https://docs.python.org/2/library/urllib2.html#urllib2.Request) class. This allows us, for example, to define custom headers.

To craft our own header we create a headers dictionary, with the header key and the custom value. Then we create a Request object to the **urlopen** function call.

For example, let's see how this works for the **User-Agent** header (which is the way the browser identifies itself) :

```python
>>> headers = {}
>>> headers['User-Agent'] = 'Googlebot'
>>> request = urllib2.Request(url, headers=headers)
>>> response = urllib2.urlopen(request)
>>> print "The Headers are: ", response.info()
The Headers are:  Date: Tue, 23 Dec 2014 15:27:01 GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=UTF-8
Set-Cookie: PREF=ID=8929a796c6fba710:FF=0:TM=1419953221:LM=1419953221:S=oEh5NKUEIEBinpwX; expires=Thu, 22-Dec-2016 15:27:01 GMT; path=/; domain=.google.com
Set-Cookie: NID=67=QhRTCRsa254cvvos3EXz8PkKnjQ6qKblw4qegtPfe1WNagQ2p0GlD1io9viogAGbFm7RVDRAieauowuaNEJS3aySZMnogy9oSvwkODi3uV3NeiHwZG_neZlu2SkO9MWX; expires=Wed, 01-Jul-2015 15:27:01 GMT; path=/; domain=.google.com; HttpOnly
P3P: CP="This is not a P3P policy! See http://www.google.com/support/accounts/bin/answer.py?hl=en&answer=151657 for more info."
Server: gws
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Alternate-Protocol: 80:quic,p=0.02
Connection: close
>>> print "The Date is: ", response.info()['date']
The Date is:  Tue, 23 Dec 2014 15:27:01 GMT
>>> print "The Server is: ", response.info()['server']
The Server is:  gws
>>> response.close()
```


We could also add headers with the **add_headers** method:

```
>>> request = urllib2.Request('http://www.google.com/')
>>> request.add_header('Referer', 'http://www.python.org/')
>>> request.add_header('User-agent', 'Mozilla/5.0')
>>> response = urllib2.urlopen(request)
```


### HTTP Authentication

When authentication is required, the server sends a header (and the **401 error code**) requesting this procedure. The response also specifies the **authentication scheme** and a **realm**. Something like this:

```
WWW-Authenticate: SCHEME realm="REALM".
```

The client then retries the request with the name and password for the realm, included as a header in the request. The steps for this process are the following:

1) create a password manager,

```
passwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
```

2) add the username and password,

```
top_url = "http://example.com/"
passwd_mgr.add_password(None, top_url, username, password)
```

3) create an auth handler,

```
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
```

4) create an *opener* (a OpenerDirector instance),

```
opener = urllib2.build_opener(handler)
```

5) use the opener to fetch a URL,

```
opener.open(a_url)
```

6) install the opener,

```
urllib2.install_opener(opener)
```

7) finally, open the page (where authentication is now handled automatically):

```
pagehandle = urllib2.urlopen(top_url)
```




### Error Handling

**urllib2** has also methods for handling URL errors:

```python
>>> request = urllib2.Request('http://www.false_server.com')
>>> try:
        urllib2.urlopen(request)
>>> except urllib2.URLError, e:
        print e.reason
(4, 'getaddrinfo failed')
```

Every HTTP response from the server contains a numeric [status code](http://en.wikipedia.org/wiki/List_of_HTTP_status_codes). The default handlers take care some of these responses and for the others, **urlopen**  raises an **HTTPError** (which is a subclass of **URLError**).


### Other Available Methods

Other available methods in the **urllib2** library:

* **install_opener** and **build_opener**: install and return an OpenDirector instance.

* ** URLError** and **HTTPError**: raises exceptions for problems, handles exotic HTTP errors, and processes [HTTP error responses](https://docs.python.org/2/howto/urllib2.html#error-codes), respectively.

* **HTTPCookieProcessor**: handles HTTP cookies.

* **HTTPProxyHandler**: sends requests to a proxy.

* **AbstractBasicAuthHandler**, **HTTPBasicAuthHandler**, **ProxyBasicAuthHandler**, **HTTPDigestAuthHandler**, **AbstractDigestAuthHandler**, **ProxyDigestAuthHandler**: handle authentications.

* **HTTPPasswordMgr** and **HTTPPasswordMgrWithDefaultRealm**: keep a database of realm, URL, user and passwords mappings.

* **HTTPHandler**, **HTTPSHandler**, **FileHandler**, **FTPHandler**, **UnknownHandler**: handle sources.


Available methods for the **Request** objects:

* **add_data**, **has_data**, and **get_data**: deal with the Request data.
* **add_header**, **add_unredirected_header**, **has_header**, **get_header**, **header_items**: deal with the header data.
* **get_full_url**, **get_type**, **get_host**, **get_selector**, **set_proxy**, **get_origin_req_host**: deal with the URL data.


And let's not forget about **urllib**'s [urlparse](http://pymotw.com/2/urlparse/index.html#module-urlparse), which provides functions to analyze URL strings. **urlparse** breaks URL strings up in several optional  components: **scheme** (example: http), **location** (example: www.python.org:80), **path** (example: index.html), **query** and **fragment**.

Other common functions are **urljoin** and **urlsplit**.




---

## <a name="map"></a>Mapping Webapps from their Installation Packages

[Content management systems](http://en.wikipedia.org/wiki/Content_management_system) are platforms to make it easy to start blogs or  simple websites. They are  common in shared host environments. However, when all of the security procedures are not followed, they can be a easy target for attackers to gain access to the server.

In this session we are going to build a scanner that searches for all files that are reachable on the remote target, following the structure of the downloaded webapp. This is based in one of the examples of [Black Hat Python](http://www.nostarch.com/blackhatpython).

This type of scanner can show installation files, directories that are not processed by [.htaccess](http://en.wikipedia.org/wiki/Htaccess), and other files that can be useful for an attack.



### Crafting the Scanner

In our scanner script, we use Python's [Queue](https://docs.python.org/2/library/queue.html) objects  to build a large stack of items and multiple threads picking items for processing. This will make the scanner run very quickly. The steps are the following:

1) We define the target URL (in this case we are borrowing the example from the book), the number of threads, the local directory where we downloaded and extracted the webapp, and a filter with the file extensions we are not interested on:

```python
import urllib2
import Queue
import os
import threading

THREADS = 10
TARGET = 'http://www.blackhatpython.com'
DIRECTORY = '/home/User/Desktop/wordpress'
FILTERS = ['.jpg', '.css', '.gif', '.png']
```

2) We define a function with a loop that keeps executing until the queue  with the paths is empty. On each iteration we get one of these paths and add it to the target URL to see whether it exists (outputting the HTTP status code):

```python
def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = '%s%s' % (TARGET, path)
        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()
            print '[%d] => %s' % (response.code, path)
            response.close()
        except urllib2.HTTPError as error:
            fail_count += 1
            print "Failed" + str(error.code)
```

3) The main loop first creates the queue for paths and then use the **os.walk** method to map all the files and directories in the local version of the webapp, adding the names to the queue (after being filtered by our custom extension list):

```python
if __name__ == '__main__':
    os.chdir(DIRECTORY)
    web_paths = Queue.Queue()
    for r, d, f in os.walk('.'):
        for files in f:
            remote_path = '%s/%s' %(r, files)
            if remote_path[0] == '.':
                remote_path = remote_path[1:]
            if os.path.splitext(files)[1] not in FILTERS:
                web_paths.put(remote_path)
```

4) Finally, we create the threads that will be sent to our function **test_remote**. The loop is kept until the path queue is empty:

```python
    for i in range(THREADS):
        print 'Spawning thread number: ' + str(i+1)
        t = threading.Thread(target=test_remote)
        t.start()
```


### Testing the Scanner

Now we are ready to test our scanner. We download and test three webapps: [WordPress](https://en-ca.wordpress.org/download/), [Drupal](https://www.drupal.org/project/download), and [Joomla 3.1.1](http://www.joomla.org/announcements/release-news/5499-joomla-3-1-1-stable-released.html).


Running first for Joomla gives the following results:

```sh
$ python mapping_web_app_install.py
Spawning thread number: 1
Spawning thread number: 2
Spawning thread number: 3
Spawning thread number: 4
Spawning thread number: 5
Spawning thread number: 6
Spawning thread number: 7
Spawning thread number: 8
Spawning thread number: 9
Spawning thread number: 10
[200] => /web.config.txt
[200] => /modules/mod_whosonline/helper.php
[200] => /LICENSE.txt
[200] => /README.txt
[200] => /modules/mod_whosonline/mod_whosonline.xml
[200] => /joomla.xml
[200] => /robots.txt.dist
(...)
```


Running for Wordpress:

```sh
(...)
[200] => /wp-links-opml.php
[200] => /index.php
[200] => /wp-config-sample.php
[200] => /wp-load.php
[200] => /license.txt
[200] => /wp-mail.php
[200] => /xmlrpc.php
[200] => /wp-trackback.php
[200] => /wp-cron.php
[200] => /wp-admin/custom-background.php
[200] => /wp-settings.php
[200] => /wp-activate.php
(...)
```

Finally, running for Drupal, we only get five files:

```sh
(...)
[200] => /download.install
[200] => /LICENSE.txt
[200] => /README.txt
[200] => /download.module
[200] => /download.info
```

In all of these results we are able to find some nice results including XML and txt files. This  recon can be the start of an attack. Really cool.




-----

## <a name="brute1"></a>Brute-Forcing the Contents of Webapps

In general we are not aware about the  structure of files that are accessible in a web server (we don't have the webapp available like in the previous example). Usually we can deploy a spider, like in the [Burp suite](http://portswigger.net/burp/),  to crawl the target and find them. However this might not be able to find sensitive files such as, for example, development/configuration files and debugging scripts.

The best way to find sensitive files is to brute-force common filenames and directories. How do we do this?

It turns out that the  task is really easy when we already have word lists for directory and files. These lists can be downloaded from sources such as the [DirBurster](https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project) project or [SVNDigger](https://www.netsparker.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/).


Since scanning third party websites is not legal, we are going to use *play* websites, which are available for testing. Some examples (from [here](http://blog.taddong.com/2011/10/hacking-vulnerable-web-applications.html)):

* [testphp.vulnweb.com](http://testphp.vulnweb.com)
* [testasp.vulnweb.com](http://testasp.vulnweb.com)
* [testaspnet.vulnweb.com](http://testaspnet.vulnweb.com)
* [testphp.vulnweb.com](http://testphp.vulnweb.com)
* [crackme.cenzic.com](http://crackme.cenzic.com)
* [google-gruyere.appspot.com/start](http://google-gruyere.appspot.com/start)
* [www.hacking-lab.com/events/registerform.html](https://www.hacking-lab.com/events/registerform.html?eventid=245)
* [hack.me](https://hack.me)
* [www.hackthissite.org](http://www.hackthissite.org)
* [zero.webappsecurity.com](http://zero.webappsecurity.com)
* [demo.testfire.net](http://demo.testfire.net)
* [www.webscantest.com](http://www.webscantest.com)
* [hackademic1.teilar.gr](hackademic1.teilar.gr)
* [pentesteracademylab.appspot.com](http://pentesteracademylab.appspot.com)


### Writing the Script
In our script we accept word lists for common names of files and directories and use them to attempt to discover reachable paths on the server.

In the same way as before, we can achieve a reasonable speed by creating pool of threads to discover the contents.

The steps of our script are:


1) We define the target, the number of threads, the path for the wordlist (which I made available [here](https://github.com/bt3gl/My-Gray-Hacker-Resources/tree/master/Other_Hackings/useful_lists/files_and_dir_lists)), a rogue User-Agent, and the filter list of extensions that we want to look at:

```python
import urllib2
import threading
import Queue
import urllib

THREADS = 10
TARGETS  = 'http://testphp.vulnweb.com'
WORDLIST_FILE = '../files_and_dir_lists/SVNDigger/all.txt'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64l rv:19.0) Gecko/20100101 Firefox/19.0'
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
```

2) We create a function that read our word list, and then add each of this words into a queue for the words, returning this queue:

```python
def build_wordlist(WORDLIST_FILE):
    f = open(WORDLIST_FILE, 'rb')
    raw_words = f.readlines()
    f.close()
    words = Queue.Queue()
    for word in raw_words:
        word = word.rstrip()
        words.put(word)
    return words
```

3) We create a function that loops over the size of the queue, checking whether it's a directory or a file (using the extension list), and then brute-forcing the target URL for each of these words:


```python
def dir_bruter(word_queue, TARGET, EXTENSIONS=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []
        if '.' not in attempt:
            attempt_list.append('/%s/' %attempt)
        else:
            attempt_list.append('/%s' %attempt)
        if EXTENSIONS:
            for extension in EXTENSIONS:
                attempt_list.append('/%s%s' %(attempt, extension))
        for brute in attempt_list:
            url = '%s%s' %(TARGET, urllib.quote(brute))
            try:
                headers = {}
                headers['User-Agent'] = USER_AGENT
                r = urllib2.Request(url, headers = headers)
                response = urllib2.urlopen(r)
                if len(response.read()):
                    print '[%d] => %s' %(response.code, url)
            except urllib2.URLError, e:
                if hasattr(e, 'code') and e.code != 404:
                    print '[! %d] => %s' %(e.code, url)
                pass
```

4) In the main loop, we build the word list and then we spawn the tread for our **dir_bruter** function:

```python
if __name__ == '__main__':
    word_queue = build_wordlist(WORDLIST_FILE)

    for i in range(THREADS):
        print 'Thread ' + str(i)
        t = threading.Thread(target=dir_bruter, args=(word_queue, target))
        t.start()
```

### Running the Script

Running this against one of the web application targets will print something like this:

```sh
$ python brute_forcing_locations.py
[200] => http://testphp.vulnweb.com/CVS
[200] => http://testphp.vulnweb.com/admin
[200] => http://testphp.vulnweb.com/script
[200] => http://testphp.vulnweb.com/images
[200] => http://testphp.vulnweb.com/pictures
[200] => http://testphp.vulnweb.com/cart.php
[200] => http://testphp.vulnweb.com/userinfo.php
!!! 403 => http://testphp.vulnweb.com/cgi-bin/
(...)
```

Pretty neat!







-----

## Further References:

- [Form Contents](http://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13.4)
- [A robot.txt parser](http://pymotw.com/2/robotparser/index.html#module-robotparser)
- [stackoverflow](http://stackoverflow.com/questions/tagged/urllib2)
- [Black Hat Python](http://www.nostarch.com/blackhatpython).
