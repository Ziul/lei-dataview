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
from pyqtgraph.Qt import QtGui, QtCore


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


def port_checker():
    global N_PORTS
    PORTS_AVAILABLE = util.available_ports()
    if N_PORTS != len(PORTS_AVAILABLE):
        util.choose_port(PORTS_AVAILABLE)
        N_PORTS = len(PORTS_AVAILABLE)

# list available ports
print 'Available ports:'
PORTS_AVAILABLE = util.available_ports()
N_PORTS = len(PORTS_AVAILABLE)
try:
    for k, i in zip(PORTS_AVAILABLE, range(N_PORTS)):
        print '%d >>> %s' % (i, k)
    print '---'
except TypeError, error:
    print "None device connected"
    exit()

# choose a port
if N_PORTS == 1:
    uc = microcontroller(PORTS_AVAILABLE[0])
elif N_PORTS == 0:
    print "None device connected"
    from sys import stdin
    uc = microcontroller(None)
    uc.readline = stdin.readline
    uc.flushInput = port_checker
    p = Plotter()
    p.newPort(uc)
elif N_PORTS > 1:
    choosed = input("Choose one:")
    print "\nChoosed: %s" % PORTS_AVAILABLE[int(choosed)]
    uc = microcontroller(PORTS_AVAILABLE[int(choosed)])
    p = Plotter()
    p.newPort(uc.serial)
    print uc.serial.readline()

timer = QtCore.QTimer()
timer.timeout.connect(port_checker)
timer.start(0)

p.setDaemon(True)
signal(SIGINT, signal_handler)
p.start()
p.join()

print 'Ready'
