#!/bin/bash

state=$1

/usr/bin/convert -delay 30 -loop 0 -resize 1200x1200 "*${state}*.png" gif/animated_${state}.gif
