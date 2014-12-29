#!/usr/bin/env python

__author__ = "bt3"

import urllib2
import Queue
import os
import threading

THREADS = 10
TARGET = 'http://www.blackhatpython.com'
# local directory into which we have downloaded and extracted the web app
#DIRECTORY = '/home/User/Desktop/Joomla'
#DIRECTORY = '/home/User/Desktop/wordpress'
DIRECTORY = '/home/User/Desktop/drupal'
# list of file extensions to not fingerprinting
FILTERS = ['.jpg', '.gif', '.png', '.css']

# each operation in the loop will keep executing until the web_paths
# Queue is empty. on each iteration we grab a path from the queue, add it
# to the target website's base path and then attempt to retrieve it
def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = '%s%s' % (TARGET, path)
        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()

            # if we are successfully retrieving the file, the output HTTP status code
            # and the full path for the file is printed
            print '[%d] => %s' % (response.code, path)
            response.close()

        # if the file is not found or protected by .htaccess, error
        except urllib2.HTTPError as error:
            fail_count += 1
            print "Failed" + str(error.code)


if __name__ == '__main__':
    os.chdir(DIRECTORY)
    # queue object where we store files to locate in the remote server
    web_paths = Queue.Queue()

    # os.walk function walks through all the files and directories in the local
    # web application directory. this builds the full path to the target files
    # and test them against filter list to make sure we are looking for the
    # files types we want. For each valid file we find, we add it to our
    # web_paths Queue.
    for r, d, f in os.walk('.'):
        for files in f:
            remote_path = '%s/%s' %(r, files)
            if remote_path[0] == '.':
                remote_path = remote_path[1:]
            if os.path.splitext(files)[1] not in FILTERS:
                web_paths.put(remote_path)


    # create a number of threads that will be called the test_remote function
    # it operates in a loop that keep executing untul the web_paths queue is
    # empty.
    for i in range(THREADS):
        print 'Spawning thread: ' + str(i)
        t = threading.Thread(target=test_remote)
        t.start()
