#!/usr/bin/python
# -*- coding:utf-8 -*-

from mock import MagicMock
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from threading import Thread
from data import DataRead
from time import sleep
import signal
import random
import sys
import select


class Plotter(Thread):

    """docstring for Plotter"""
    alive = False
    N_SENSOR = 0
    MAX = 50
    devices = {'ports': [],
               'data': [],
               'plot': []}

    def __init__(self):
        super(Plotter, self).__init__()
        self.name = 'Plotter'
        self.app = QtGui.QApplication([])
        # mw = QtGui.QMainWindow()
        # mw.resize(800, 800)
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Dataview Plots')

    def start(self):
        self.alive = True
        signal.signal(signal.SIGINT, self.stop)
        # super(Plotter, self).start()
        self.run()

    def join(self, time=0):
        print 'oi'
        if(time != 0):
            super(Plotter, self).join(time)
        else:
            while self.alive:
                pass
        self.stop()

    def stop(self, signal=0, frame=0):
        self.alive = False
        sleep(0.5)

    def newPort(self, port):
        self.devices['ports'].append(port)
        p = self.win.addPlot(title="Device %s" % len(self.devices['ports']))
        # p.addLegend()
        self.devices['plot'].append(p)

    def readline(self, port):
        data = ''
        datastore = DataRead(data)
        while True:
            line = port.readline()
            if line != '\n':
                data += line
            else:
                obj = datastore.read(data)
                break
        try:
            self.time = obj.time
            return obj.data
        except Exception:
            pass

    def update(self):

        for port, plot in zip(self.devices['ports'], self.devices['plot']):
            msg = self.readline(port)
            if msg != '':
                plot.clear()
                plot.setLabel('bottom', text=self.time)
                for data, i, udata in zip(self.devices['data'],
                                          range(self.N_SENSOR),
                                          msg):

                    data.append(udata)
                    if len(data) > self.MAX:
                        del data[0]

                    p = plot.plot(
                        data, pen=(i, self.N_SENSOR), name = "Sensor %d" % i)

    def run(self):

        # If none port connected
        if len(self.devices['ports']) == 0:
            self.stop()
            raise Exception(" None port included")

        # Flush input to avoid mess
        for port in self.devices['ports']:
            port.flushInput()

        sys.stderr.write("Reading first data\n")
        msg = self.readline(self.devices['ports'][0])

        try:
            self.N_SENSOR = len(msg)
        except TypeError:
            sys.stderr.write(msg + '\n')
            raise

        for i in range(self.N_SENSOR):
            self.devices['data'].append([0])
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

        while self.alive:
            pass


def signal_handler(signal, frame):

    sys.stderr.write('\nCtrl+C  pressed!\n\n')
    p.stop()


def main():
    # signal.signal(signal.SIGINT, signal_handler)
    port = MagicMock()
    port.readline = sys.stdin.readline
    p.newPort(port)
    p.start()
    p.join()

if __name__ == '__main__':
    p = Plotter()
    p.setDaemon(True)
    main()
