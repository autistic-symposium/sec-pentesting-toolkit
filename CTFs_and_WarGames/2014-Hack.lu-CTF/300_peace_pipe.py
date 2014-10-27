import socket

PORTc = 1432
PORTm = 1434
PORTw = 1433
HOST = 'wildwildweb.fluxfingers.net'

def peace_pipe():

    """ Get the magic message from some user to calculate rm """

    # create sockets
    sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to w
    sw.connect((HOST, PORTw))
    sw.recv(4096)
    sw.send(b'makawee')
    sw.recv(4096)
    sec = sw.recv(4096)
    tw = sec.split("did this:")[1].split("\n")[1].strip()
    print "\nMagic from w to m: " + tw

    # connect to m
    sm.connect((HOST, PORTm))
    sm.recv(4096)
    sm.send(b'mrblack')
    sm.recv(4096)
    sec = sm.recv(4096)
    tm = sec.split("did this:")[1].split("\n")[1].strip()
    print "\nMagic from m to w: " + tm

    # send w's magic to m's
    sm.send(tw)
    print sm.recv(4096)

    # send m's magic to get the token
    sw.send(tm)
    token = sw.recv(4096)
    token = token.split('\n')[1].strip()
    print "Token is: " + token

    # finally, send token back to m
    sm.send(token)
    print sm.recv(4096)

    sm.close()
    sw.close()


if __name__ == "__main__":
    peace_pipe()
