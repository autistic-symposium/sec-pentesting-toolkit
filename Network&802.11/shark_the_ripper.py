#!/usr/bin/env python

import os
import sys
import binascii

"""
    Shark the Ripper Tool

    For packet capture CTF problems:
        Follow TCP Steam > Hex Dump > (Select Client/Server Chat) > Save As
        Then input the file, followed by offset(s) where you want to cut.

    -mandy

"""

if len(sys.argv) < 2:
    print "Oh ffs, seriously?"
    print "Usage: " + sys.argv[0] + " pasted_wireshark_hex_dump.txt START_OFFSET END_OFFSET"
    sys.exit()

if os.path.isfile( sys.argv[1] ):
    with open( sys.argv[1] ) as f:
        filecontents = f.read()

    if len( sys.argv ) > 2:
        if len( sys.argv ) == 4:
            start = sys.argv[2]
            end = sys.argv[3]
        else:
            start = sys.argv[2]
            end = "FFFFFFFF"

        cut = True

        if len( start ) != 8 or len( end ) != 8:
            print "Invalid offset size"
            sys.exit()
    else:
        cut = False

    output = ""

    if cut == True:
        start_cutting = False
        for row in filecontents.split("\n"):
            if row != "":
                if row[:8] == start:
                    start_cutting = True

                if row[:8] == end:
                    start_cutting = False

                if start_cutting == True:
                    output += row[10:][:48].replace(" ", "")
    else:
        for row in filecontents.split("\n"):
            if row != "":
                output += row[10:][:48].replace(" ", "")

    output = binascii.unhexlify(output)
    with open( sys.argv[1] + ".out", 'w') as output_file:
        output_file.write( output )

