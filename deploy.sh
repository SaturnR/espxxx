#!/usr/bin/env bash

ampy -p /dev/ttyUSB0 --baud 115200 put mfrc522.py; lcd examples; put read.py; put write.py; ls
