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


def signal_handler(signal=0, frame=0):

    sys.stderr.write('\nCtrl+C  pressed!\n\n')
    exit()

color = 2
b = range(10)


def update():
    global color, b
    a = random.randint(10, 200)
    b.append(a)
    if len(b) > 30:
        b = b[1:]
    p.setData(b[10:])


def includer():
    win.nextRow()
    x = range(10)
    y = range(10)
    curve1 = win.addPlot(title='teste')
    curve1.plot(x, y)

app = QtGui.QApplication([])
# mw = QtGui.QMainWindow()
# mw.resize(800, 800)
win = pg.GraphicsWindow()
win.setWindowTitle('Scrolling Plots')

x = range(10)
y = range(10)
plotWidget = win.addPlot()
p = plotWidget.plot(x, y)

win.nextRow()
curve1 = win.addPlot()
curve1.plot(x, y)


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)

inc = QtCore.QTimer()
inc.timeout.connect(includer)
inc.start(3000)


quiter = QtCore.QTimer()
quiter.timeout.connect(signal_handler)
quiter.start(7000)

signal.signal(signal.SIGINT, signal_handler)
if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()
