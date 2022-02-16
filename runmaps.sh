#!/bin/bash

set -e

state=$1

#./hydromap.py 2 $1
./hydromap.py 4 $1
./hydromap.py 6 $1
./hydromap.py 8 $1
./hydromap.py 10 $1
#./hydromap.py 12 $1

# /usr/local/bin/convert -delay 30 -loop 0 "*${state}*.pdf" animated_${state}.gif
