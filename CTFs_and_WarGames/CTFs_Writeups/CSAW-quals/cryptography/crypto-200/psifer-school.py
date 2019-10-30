#!/usr/bin/env python


__author__ = "bt3gl"


import sys
from telnetlib import Telnet
from caesarCipher import decipher, decipher_simple
from pygenere import VigCrack



def solve1(msg):
  # Caesar Cipher
  # Solve the first cypher and encode back to unicode:
  # the method encode() returns an encoded version of the string
  # Both method work fine.
  # One is by freq. analysis or the other by rotating
  dec_msg = decipher(msg)
  #dec_msg = decipher_simple(msg)
  dec_msg = dec_msg.split()[-1]
  return dec_msg




def solve2(msg):
  msg="I'lcslraooh o rga tehhywvf.retFtelh mao ae  af ostloh lusr bTsfnr, epawlltddaheoo  aneviedr ose rtyyng etn aini ft oooey hgbifecmoswuut!oa eeg   ar rr h.u t. hylcg io we ph ftooriysneirdriIa utyco gfl oostif sp u"+'""'+"flcnb  roh tprn.o h"
  # Shift cypher, but dealing with special characters
  for j in range(2, len(msg)):

    dec_msg = ['0'] * len(msg)
    idec_msg, shift = 0, 0

    for i in range(len(msg)):
      dec_msg[idec_msg] = msg[i]
      idec_msg += j

      if idec_msg >  len(msg) - 1:
        shift += 1
        idec_msg = shift
    dec_msg = "".join(dec_msg)

    if "you" not in dec_msg: continue
    return dec_msg




def solve3(msg):
  # Vigenere Cypher
  key =  VigCrack(msg).crack_codeword()
  dec_msg = VigCrack(msg).crack_message()
  dec_msg =  dec_msg.replace(" ", "")
  return key, dec_msg





if __name__ == '__main__':

  """
  PORT = 12345
  HOST = '54.209.5.48'
  tn = Telnet(HOST ,PORT)


  '''
    SOLVING STAGE 1 - CEASAR CIPHER
  '''

  tn.read_until(b'psifer text: ')
  msg_in1 = tn.read_until(b'\n').dec_msg().strip()

  answer1 = solve1(msg_in1)

  tn.write(answer1.encode() + b'\n')

  print 'Message stage 1: ' + msg_in1
  print
  print 'Answer stage 1: ' + answer1
  print
  print



  '''
    SOLVING STAGE 2 - SPECIAL CHARS
  '''
  msg_in2 = tn.read_all().dec_msg()
  msg_in2 = (msg_in2.split(':')[1]).split("Time")[0]

  answer2 = solve2(msg_in2)

  tn.write(answer2.encode() + b'\n')

  print 'Message stage 2: ' + msg_in2
  print
  print 'Answer stage 2: ' + answer2
  print
  print


  '''
    SOLVING STAGE 3 - VINEGERE
  '''
  msg_in3 = tn.read_all().dec_msg()
  msg_in3 = (msg_in3.split(':')[1]).split("Time")[0]


  key, answer3 = solve3(msg_in3)
  tn.write(answer3.encode() + b'\n')

  print 'Message stage 3: ' + msg_in3
  print
  print 'Answer stage 3: ' + answer3
  print '(key: ' + key + ')'

  """ 
  print solve2(msg='a')
