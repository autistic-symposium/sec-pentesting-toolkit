#!/usr/bin/env python3 -O

import argparse
import subprocess
import sys

def usage():
  print("%s target_host target_port" % sys.argv[0])

if len(sys.argv) < 3:
  usage()
  sys.exit(1)

target_host = sys.argv[1]
target_port = sys.argv[2]


KEX_ALGORITHMS = {
    'curve25519-sha256@libssh.org':         [],
    'diffie-hellman-group-exchange-sha256': [],

    'diffie-hellman-group-exchange-sha1': [ 'Weak hash' ],
    'diffie-hellman-group14-sha1':        [ 'Weak hash' ],
    'ecdh-sha2-nistp521':                 [ 'BULLRUN' ],
    'ecdh-sha2-nistp384':                 [ 'BULLRUN' ],
    'ecdh-sha2-nistp256':                 [ 'BULLRUN' ],
    'diffie-hellman-group1-sha1':         [ 'Small modulus', 'Weak hash' ],
}

HOST_KEY_ALGORITHMS = {
    'ssh-ed25519-cert-v01@openssh.com': [],
    'ssh-rsa-cert-v01@openssh.com':     [],
    'ssh-rsa-cert-v00@openssh.com':     [],
    'ssh-ed25519':                      [],
    'ssh-rsa':                          [],
 
    'ecdsa-sha2-nistp521-cert-v01@openssh.com': [ 'BULLRUN' ],
    'ecdsa-sha2-nistp384-cert-v01@openssh.com': [ 'BULLRUN' ],
    'ecdsa-sha2-nistp256-cert-v01@openssh.com': [ 'BULLRUN' ],
    'ecdsa-sha2-nistp521':                      [ 'BULLRUN' ],
    'ecdsa-sha2-nistp384':                      [ 'BULLRUN' ],
    'ecdsa-sha2-nistp256':                      [ 'BULLRUN' ],
    'ssh-dss-cert-v01@openssh.com':             [ 'Small modulus', 'BULLRUN' ],
    'ssh-dss-cert-v00@openssh.com':             [ 'Small modulus', 'BULLRUN' ],
    'ssh-dss':                                  [ 'Small modulus', 'BULLRUN' ],
}

CIPHERS = {
    'chacha20-poly1305@openssh.com': [],
    'aes256-gcm@openssh.com':        [],
    'aes128-gcm@openssh.com':        [],
    'aes256-ctr':                    [],
    'aes192-ctr':                    [],
    'aes128-ctr':                    [],
    
    'aes256-cbc':                  [ 'CBC mode' ],
    'rijndael-cbc@lysator.liu.se': [ 'CBC mode' ],
    'aes192-cbc':                  [ 'CBC mode' ],
    'aes128-cbc':                  [ 'CBC mode' ],
    'blowfish-cbc':                [ 'Small block size', 'CBC mode' ],
    'cast128-cbc':                 [ 'Small block size', 'CBC mode' ],
    '3des-cbc':                    [ 'Weak cipher', 'Small block size', 'CBC mode' ],
    'arcfour256':                  [ 'Weak cipher' ],
    'arcfour128':                  [ 'Weak cipher' ],
    'arcfour':                     [ 'Weak cipher', 'Small key size' ],
    'none':                        [ 'Holy shit, plaintext' ],
}

MACS = {
    'hmac-sha2-512-etm@openssh.com':  [],
    'hmac-sha2-256-etm@openssh.com':  [],
    'umac-128-etm@openssh.com':       [],
    'hmac-ripemd160-etm@openssh.com': [],
    'hmac-sha2-512':                  [ 'Encrypt-and-MAC' ],
    'hmac-sha2-256':                  [ 'Encrypt-and-MAC' ],
    'hmac-ripemd160':                 [ 'Encrypt-and-MAC' ],
    'umac-128@openssh.com':           [ 'Encrypt-and-MAC' ],

    'umac-64-etm@openssh.com':      [ 'Small tag size' ],
    'umac-64@openssh.com':          [ 'Encrypt-and-MAC', 'Small tag size' ],
    'hmac-sha1-etm@openssh.com':    [ 'Weak hash' ],
    'hmac-sha1':                    [ 'Weak hash', 'Encrypt-and-MAC' ],
    'hmac-sha1-96-etm@openssh.com': [ 'Weak hash', 'Small tag size' ],
    'hmac-sha1-96':                 [ 'Weak hash', 'Encrypt-and-MAC', 'Small tag size' ],
    'hmac-md5-etm@openssh.com':     [ 'Weak hash' ],
    'hmac-md5-96-etm@openssh.com':  [ 'Weak hash', 'Small tag size' ],
    'hmac-md5':                     [ 'Weak hash', 'Encrypt-and-MAC' ],
    'hmac-md5-96':                  [ 'Weak hash', 'Encrypt-and-MAC', 'Small tag size' ],
}

def ssh(host, port, **kwargs):
    cmd = [ '/usr/bin/ssh' ]

    for ( key, value ) in kwargs.items():
        cmd.append('-o')
        cmd.append(key + '=' + ','.join(value))

    cmd.append('-p')
    cmd.append(str(port))
    cmd.append(host)
    cmd.append('/bin/true')
    proc = subprocess.Popen(cmd)
    return proc.wait() == 0

print('# Testing key exchange')
for ( kex, problems ) in KEX_ALGORITHMS.items():
    allowed = ssh(
        target_host, target_port,
        KexAlgorithms     = [ kex ],
        HostKeyAlgorithms = HOST_KEY_ALGORITHMS.keys(),
        Ciphers           = CIPHERS.keys(),
        MACs              = MACS.keys()
    )

    if allowed and len(problems) > 0:
        print('KexAlgorithms {} # {}'.format(kex, ', '.join(problems)))

print('# Testing server authentication')
for ( hostkey, problems ) in HOST_KEY_ALGORITHMS.items():
    allowed = ssh(
        target_host, target_port,
        KexAlgorithms      = KEX_ALGORITHMS.keys(),
        HostKeyAlgorithms  = [ hostkey ],
        Ciphers            = CIPHERS.keys(),
        MACs               = MACS.keys(),
        UserKnownHostsFile = [ 'known_hosts_' + hostkey ]
    )

    if allowed and len(problems) > 0:
        print('HostKeyAlgorithms {} # {}'.format(hostkey, ', '.join(problems)))

allowed_ciphers = set()

print('# Testing symmetric ciphers')
for ( cipher, problems ) in CIPHERS.items():
    allowed = ssh(
        target_host, target_port,
        KexAlgorithms     = KEX_ALGORITHMS.keys(),
        HostKeyAlgorithms = HOST_KEY_ALGORITHMS.keys(),
        Ciphers           = [ cipher ],
        MACs              = MACS.keys()
    )
    always_bad = [ p for p in problems if p != 'CBC mode' ]
    maybe_bad = [ p for p in problems if p == 'CBC mode' ]

    if allowed:
        if len(always_bad) > 0:
            print('Ciphers {} # {}'.format(cipher, ', '.join(problems)))

        if len(maybe_bad) > 0:
            allowed_ciphers.add(cipher)

allowed_macs = set()

print('# Testing message authentication codes')
for ( mac, problems ) in MACS.items():
    allowed = ssh(
        target_host, target_port,
        KexAlgorithms     = KEX_ALGORITHMS.keys(),
        HostKeyAlgorithms = HOST_KEY_ALGORITHMS.keys(),
        Ciphers           = CIPHERS.keys(),
        MACs              = [ mac ]
    )
    always_bad = [ p for p in problems if p != 'Encrypt-and-MAC' ]
    maybe_bad = [ p for p in problems if p == 'Encrypt-and-MAC' ]

    if allowed:
        if len(always_bad) > 0:
            print('MACs {} # {}'.format(mac, ', '.join(problems)))

        if len(maybe_bad) > 0:
            allowed_macs.add(mac)

print('# Testing problematic cipher and MAC combinations')
for cipher in allowed_ciphers:
    for mac in allowed_macs:
        print('## Dangerous combination of CBC and Encrypt-and-MAC')
        print('Ciphers {} # {}'.format(cipher, ', '.join(CIPHERS[cipher])))
        print('MACs {} # {}'.format(mac, ', '.join(MACS[mac])))
