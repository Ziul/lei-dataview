#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the speed of rapidly updating multiple plot curves
"""

# Add path to library (just for examples; you do not need this)
# import initExample


from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import numpy as np
import signal
import random

import serial
from dataview.scanf import sscanf
from dataview.scanf import IncompleteCaptureError

color = 2
x = range(10)
y = range(10)
z = range(10)
tty = serial.Serial(timeout=0)

def signal_handler(signal=0, frame=0):

    sys.stderr.write('\nCtrl+C  pressed!\n\n')
    exit()

def update():
    global color, tty,x,y,z
    formatter = "x1:  %d y1:  %d z1:  %d"
    #a = random.randint(10, 200)
    loaded = tty.readline()
    try:
        a= sscanf(loaded, formatter)
        x.append(a[0])
        y.append(a[1])
        z.append(a[2])
        print a
    except IncompleteCaptureError:
        #print loaded
        pass
    except Exception, e:
        raise e
    
    if len(x) > 100:
        x = x[1:]
    p.setData(x)

    if len(y) > 100:
        y = y[1:]
    q.setData(y)


    if len(z) > 100:
        z = z[1:]
    r.setData(z)



tty.baudrate = 9600
tty.port = '/dev/ttyACM0'
tty.open()


app = QtGui.QApplication([])
# mw = QtGui.QMainWindow()
# mw.resize(800, 800)
win = pg.GraphicsWindow()
win.setWindowTitle('Scrolling Plots')

x = range(10)
y = range(10)
plotWidgetx = win.addPlot()
plotWidgetx.setRange(yRange=[300, 550])
p = plotWidgetx.plot(x, y)

win.nextRow()
plotWidgety = win.addPlot()
plotWidgety.setRange(yRange=[300, 550])
q = plotWidgety.plot(x, y)

win.nextRow()
plotWidgetz = win.addPlot()
plotWidgetz.setRange(yRange=[300, 550])
r = plotWidgetz.plot(x, y)





timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

quiter = QtCore.QTimer()
quiter.timeout.connect(signal_handler)
#quiter.start(7000)

signal.signal(signal.SIGINT, signal_handler)
if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()
