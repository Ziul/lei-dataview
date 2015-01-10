#!/usr/bin/python2.7

# cmd = "socat -lflog.log -d -d pty,raw,echo=0 pty,raw,echo=0"

import subprocess
from sys import argv

usbs = argv[1:]

f = open('log.log', 'r').read().split()

ports = []
for i in f:
    if '/dev/pts' in i:
        ports.append(i)

output = ''
for i, p in zip(ports, usbs):
    data = "ln -s %s /dev/ttyUSB%s" % (i, p)
    output += data + '\n'
    subprocess.Popen(data.split())
    data = "chmod 666 /dev/ttyUSB%s" % p
    subprocess.Popen(data.split())

print output

# subprocess.Popen('killall socat -9'.split())
