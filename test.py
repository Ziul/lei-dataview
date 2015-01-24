#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the speed of rapidly updating multiple plot curves
"""

# Add path to library (just for examples; you do not need this)
# import initExample


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

import serial
from dataview.device import util
from dataview.data import DataRead
# QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
# mw.resize(800,800)

p = pg.plot()
p.setWindowTitle('DataView')
#p.setRange(QtCore.QRectF(0, -10, 5000, 20))
p.setLabel('bottom', 'Index', units='B')

nPlots = 10
nSamples = 500
#curves = [p.plot(pen=(i,nPlots*1.3)) for i in range(nPlots)]
curves = []
for i in range(nPlots):
    c = pg.PlotCurveItem(pen=(i, nPlots * 1.3))
    p.addItem(c)
    c.setPos(0, i * 6)
    curves.append(c)

p.setYRange(0, nPlots * 6)
p.setXRange(0, nSamples)
p.resize(600, 900)

rgn = pg.LinearRegionItem([nSamples / 5., nSamples / 3.])
p.addItem(rgn)


# data = np.random.normal(size=(nPlots * 23, nSamples))
data = []
ptr = 0
lastTime = time()
fps = None
count = 0
uc = object()


def read_data_uc():
    global uc, nPlots
    data = ''
    datastore = DataRead(data)
    while True:
        line = uc.readline()
        if line != '\n':
            data += line
        else:
            ret = datastore.read(data)
            nPlots = len(ret.data)
            return ret


def update():
    global curve, data, ptr, p, lastTime, fps, nPlots, count, uc
    count += 1
    # print "---------", count
    data.append(read_data_uc().data)
    for i, d in zip(range(nPlots), data):
        curves[i].setData(d)

    # print "   setData done."
    ptr += nPlots
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0 / dt
    else:
        s = np.clip(dt * 3., 0, 1)
        fps = fps * (1 - s) + (1.0 / dt) * s
    p.setTitle('%0.2f fps' % fps)
    # app.processEvents()  ## force complete redraw for every plot


def signal_handler(signal, frame):

    sys.stderr.write('\nCtrl+C  pressed!\n\n')
    exit()

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    import signal
    signal.signal(signal.SIGINT, signal_handler)

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
        exit()
    elif len(PORTS_AVAILABLE) > 1:
        choosed = input("Choose one:")
        print "\nChoosed: %s" % PORTS_AVAILABLE[int(choosed)]
        uc = serial.Serial(PORTS_AVAILABLE[int(choosed)], 9600, timeout=0)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(0)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
