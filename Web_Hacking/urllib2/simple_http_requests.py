#!/usr/bin/env python

__author__ = "bt3"

import urllib2
import urllib

def post_general(url):
    values = {'name' : 'Dana Scullt',
              'location' : 'Virginia',
              'language' : 'Python' }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    print response.read()


def get_general(url):
    msg = urllib2.urlopen(url)
    print msg.read()


def get_fancy(url):
    response = urllib2.urlopen(url)
    print 'RESPONSE:', response
    print 'URL     :', response.geturl()

    headers = response.info()
    print 'DATE    :', headers['date']
    print 'HEADERS :'
    print '---------'
    print headers

    data = response.read()
    print 'LENGTH  :', len(data)
    print 'DATA    :'
    print '---------'
    print data



def get_user_agent(url):
    headers = {}
    headers['User-Agent'] = 'Googlebot'

    request = urllib2.Request(url, headers=headers)
    request = urllib2.Request('http://www.google.com/')
    request.add_header('Referer', 'http://www.python.org/')
    request.add_header('User-agent', 'Mozilla/5.0')
    response = urllib2.urlopen(request)

    #print response.read()
    print "The Headers are: ", response.info()
    print "The Date is: ", response.info()['date']
    print "The Server is: ", response.info()['server']
    response.close()


def error(url):
    request = urllib2.Request('http://aaaaaa.com')
    try:
        urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':

    HOST = 'http://www.google.com'

    #get_user_agent(HOST)
    #get_fancy(HOST)
    #post_general(HOST)
    #get_user_agent(HOST)
    error(HOST)