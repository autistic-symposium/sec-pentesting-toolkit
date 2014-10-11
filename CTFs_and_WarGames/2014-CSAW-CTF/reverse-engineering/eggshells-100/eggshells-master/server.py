import utils
import socket

import time
import sys


def interact(conn, addr):
    command = ''
    print "Received", addr

    while (command != 'exit'):
        command = raw_input('> ')
        conn.send(command + '\n')
        time.sleep(.5)
        data = conn.recv(0x10000)
        if not data:
            print "Disconnected", addr
            return
        print data.strip(),
    else:
        print "Disconnected", addr


HOST = ''

PORT = 6969

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

s.listen(1)

while 1:
    conn, addr = s.accept()
    interact(conn, addr)

    

    
