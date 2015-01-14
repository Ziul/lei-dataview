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


def signal_handler(signal, frame):

    sys.stderr.write('\nCtrl+C  pressed!\n\n')
    p.stop()


# list available ports
print 'Available ports:'
PORTS_AVAILABLE = util.available_ports()
try:
    for i in PORTS_AVAILABLE:
        print '>>> %s' % i
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
    uc.readline = stdin
    # exit()

p = Plotter(read_data)
p.setDaemon(True)
signal(SIGINT, signal_handler)
p.start()
p.join()

print 'Ready'
