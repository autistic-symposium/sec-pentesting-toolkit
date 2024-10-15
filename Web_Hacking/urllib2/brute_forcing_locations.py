#!/usr/bin/env python

__author__ = "bt3"

import urllib2
import threading
import Queue
import urllib

THREADS = 10
TARGETS  = [ 'http://testphp.vulnweb.com', \
            'http://testasp.vulnweb.com', \
            'http://testaspnet.vulnweb.com',\
            'http://testphp.vulnweb.com',\
            'http://crackme.cenzic.com',\
            'http://google-gruyere.appspot.com/start',\
            'https://www.hacking-lab.com/events/registerform.html?eventid=245',\
            'https://hack.me',\
            'http://www.hackthissite.org',\
            'http://zero.webappsecurity.com',\
            'http://demo.testfire.net',\
            'http://www.webscantest.com',\
            'http://hackademic1.teilar.gr',\
            'http://pentesteracademylab.appspot.com']

WORDLIST_FILE = '../files_and_dir_lists/SVNDigger/all.txt'
RESUME = None
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64l rv:19.0) Gecko/20100101 Firefox/19.0'
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']

# read the wordlist and iteract over each line
def build_wordlist(WORDLIST_FILE):
    f = open(WORDLIST_FILE, 'rb')
    raw_words = f.readlines()
    f.close()

    found_resume = False
    words = Queue.Queue()

    for word in raw_words:
        word = word.rstrip()

        # functionality that allows to resume a brute-forcing
        # session if the network connectivity is interrupted or down
        if RESUME is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print 'Resuming wordlist from: ' + resume
        else:
            words.put(word)
    # when the entire file has been parsed, we return a Queue full of
    # words to use on the brute-forcing function
    return words

# accepts a Queue object that is populated with words to use
# for brute-forcing and an optional list of files extensions to test
def dir_bruter(word_queue, TARGET, EXTENSIONS=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        # check to see if there is a file extension,
        # if not, its a directory
        # see if there is a file extension in the current word
        if '.' not in attempt:
            attempt_list.append('/%s/' %attempt)
        else:
            attempt_list.append('/%s' %attempt)

        # if we want to bruteforce extensions, apply to the current word
        if EXTENSIONS:
            for extension in EXTENSIONS:
                attempt_list.append('/%s%s' %(attempt, extension))

        # iterate over our lists of attempts
        for brute in attempt_list:
            url = '%s%s' %(TARGET, urllib.quote(brute))
            try:
                headers = {}
                # set to something innocuous
                headers['User-Agent'] = USER_AGENT
                r = urllib2.Request(url, headers = headers)

                # test the remote web server
                response = urllib2.urlopen(r)
                if len(response.read()):
                    print '[%d] => %s' %(response.code, url)
            except urllib2.URLError, e:
                if hasattr(e, 'code') and e.code != 404:
                    print '[! %d] => %s' %(e.code, url)
                pass


if __name__ == '__main__':
    # get the list, and spin threads to brute force it
    word_queue = build_wordlist(WORDLIST_FILE)

    for target in TARGETS:
        #print "Attacking " + target + '...'
        for i in range(THREADS):
            print 'Thread ' + str(i)
            t = threading.Thread(target=dir_bruter, args=(word_queue, target))
            t.start()