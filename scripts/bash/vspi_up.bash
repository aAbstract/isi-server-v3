#!/bin/bash

sudo socat -dd pty,raw,echo=0,link=/dev/ttyUSB0,mode=777 pty,raw,echo=0,link=/dev/ttyUSB1,mode=777
socat -dd TCP-LISTEN:6543,reuseaddr,fork FILE:/dev/ttyUSB0,raw,echo=0
