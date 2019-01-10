#!/usr/bin/env python3

import socket
import sys


color = sys.argv[2]
r, g, b = eval('0x'+color[0]), eval('0x'+color[1]), eval('0x'+color[2])

file_name = sys.argv[1]

s = socket.socket()

s.connect(('192.168.4.1', 5555))

f = open(file_name, 'rb')
data = f.read()

data = data.decode(encoding='utf-8')

data = data.format(1023 - int(r*68.2), 1023 - int(g*68.2), 1023 - int(b*68.2))

data = bytes(data, encoding='utf-8')

data = b'#!remote\n' + data + b'#<!>remote'

print(data)
s.sendall(data)
print(s.recv(1024))

s.close()
