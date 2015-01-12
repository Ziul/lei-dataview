#!/usr/bin/python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
from threading import Thread
from data import DataRead
from time import sleep
import signal
import random
import sys


class Plotter(Thread):

    """docstring for Plotter"""
    alive = False
    time = []
    MAX = 50

    def __init__(self, readermethod):
        super(Plotter, self).__init__()
        self.read = readermethod
        self.name = 'Plotter'

    def start(self):
        self.alive = True
        signal.signal(signal.SIGINT, self.stop)
        # super(Plotter, self).start()
        self.run()

    def join(self, time=0):
        if(time != 0):
            super(Plotter, self).join(time)
        else:
            while self.alive:
                sleep(0.1)
        self.stop()

    def stop(self, signal=0, frame=0):
        self.alive = False
        sleep(0.5)

    def readline(self):
        obj = self.read()
        try:
            # self.time.append(obj.time)
            # if len(self.time) > self.MAX:
            #     self.time = self.time[1:]
            self.time = obj.time
            return obj.data
        except Exception:
            pass

    def run(self):
        N_ADC = 10
        fig = plt.figure(figsize=(16, 10))
        axis = fig.add_subplot(111)
        axis.set_xlim([0, self.MAX + 5])
        plt.ion()
        plt.show()
        sys.stderr.write("Reading first data\n")
        msg = self.readline()
        msg = self.readline()
        if (len(msg)) != N_ADC:
            N_ADC = len(msg)
        self.ADC = {"label": [], 'values': [], 'axis': range(N_ADC)}
        for i in range(N_ADC):
            self.ADC['label'].append("Sensor " + str(i + 1))
            self.ADC['values'].append([])
            self.ADC['axis'][i], = (
                axis.plot(self.ADC['values'][i]))

        fig.legend(self.ADC['axis'], self.ADC['label'])
        while self.alive:
            try:
                msg = self.readline()
                for i in range(N_ADC):
                    self.ADC['values'][i].append(float(msg[i]))
                    if(len(self.ADC['values'][i]) > self.MAX):
                        self.ADC['values'][i] = self.ADC['values'][i][1:]
                    self.ADC['axis'][i].set_ydata(self.ADC['values'][i])
                    self.ADC['axis'][i].set_xdata(
                        range(len(self.ADC['values'][i])))
                axis.relim()
                axis.autoscale_view(True, True, True)
                plt.xlabel(self.time)
                # print msg
            except ValueError:
                sys.stderr.write(
                    "Dado mal formatado " + str(msg) + "\n")
            except IndexError:
                sys.stderr.write("\rÍndice " + str(i) + " inexistente\n")
                pass
            except TypeError:
                sys.stderr.write("\rNo new value [%s]" % str(msg))
                sleep(0.5)
                # self.stop()  # comment to let it roll
            plt.draw()


def signal_handler(signal, frame):

    sys.stderr.write('\nCtrl+C pressionado!\n\n')
    p.stop()


def f(arg=0):
    # print('oi')
    data = ''
    datastore = DataRead(data)
    for line in sys.stdin:
        if line != '\n':
            data += line
        else:
            ret = datastore.read(data)
            return ret


def main():
    signal.signal(signal.SIGINT, signal_handler)
    p.start()
    p.join()

if __name__ == '__main__':
    p = Plotter(f)
    p.setDaemon(True)
    main()
