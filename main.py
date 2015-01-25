#!/usr/bin/python
# -*- coding:utf-8 -*-

from dataview import dependencies

if dependencies.check() is False:
    exit()


from dataview.device import util
from dataview.plot import Plotter
from dataview.device.arduino import Arduino as microcontroller
from dataview.data import DataRead
from signal import signal, SIGINT


def read_data():
    data = ''
    datastore = DataRead(data)
    for line in stdin:
        if line != '\n':
            data += line
        else:
            ret = datastore.read(data)
            return ret


def read_data_uc():
    data = ''
    datastore = DataRead(data)
    while True:
        line = uc.serial.readline()
        if line != '\n':
            data += line
        else:
            ret = datastore.read(data)
            return ret


def signal_handler(signal, frame):

    sys.stderr.write('\nCtrl+C  pressed!\n\n')
    p.stop()


# list available ports
print 'Available ports:'
PORTS_AVAILABLE = util.available_ports()
try:
    for k, i in zip(PORTS_AVAILABLE, range(len(PORTS_AVAILABLE))):
        print '%d >>> %s' % (i, k)
    print '---'
except TypeError, error:
    print "None device connected"
    exit()

# choose a port
if len(PORTS_AVAILABLE) == 1:
    uc = microcontroller(PORTS_AVAILABLE[0])
elif len(PORTS_AVAILABLE) == 0:
    print "None device connected"
    from sys import stdin
    uc = microcontroller(None)
    uc.readline = stdin.readline
    p = Plotter()
    p.newPort(uc)
elif len(PORTS_AVAILABLE) > 1:
    choosed = input("Choose one:")
    print "\nChoosed: %s" % PORTS_AVAILABLE[int(choosed)]
    uc = microcontroller(PORTS_AVAILABLE[int(choosed)])
    p = Plotter()
    p.newPort(uc.serial)
    print uc.serial.readline()

p.setDaemon(True)
signal(SIGINT, signal_handler)
p.start()
p.join()

print 'Ready'
