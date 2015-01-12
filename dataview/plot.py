#!/usr/bin/python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
from threading import Thread
from data import DataRead
import signal
import random
import sys


class Plotter(Thread):

    """docstring for Plotter"""
    alive = False
    MAX = 50

    def __init__(self, readermethod):
        super(Plotter, self).__init__()
        self.readline = readermethod
        self.name = 'Plotter'

    def start(self):
        self.alive = True
        signal.signal(signal.SIGINT, self.stop)
        super(Plotter, self).start()

    def stop(self):
        self.alive = False

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
        if (len(msg)) < N_ADC:
            sys.stderr.write("Wating more sensors\n")
            N_ADC = len(msg)
        ADC = {"label": [], 'values': [], 'axis': range(N_ADC)}
        for i in range(N_ADC):
            ADC['label'].append("Sensor_" + str(i))
            ADC['values'].append([]
                                 )
            ADC['axis'][i], = (axis.plot(ADC['values'][i]))
        fig.legend(ADC['axis'], ADC['label'])
        while self.alive:
            try:
                msg = self.readline()
                for i in range(N_ADC):
                    ADC['values'][i].append(float(msg[i]))
                    if(len(ADC['values'][i]) > self.MAX):
                        ADC['values'][i] = ADC['values'][i][1:]
                    ADC['axis'][i].set_ydata(ADC['values'][i])
                    ADC['axis'][i].set_xdata(range(len(ADC['values'][i])))
                    axis.relim()
                    axis.autoscale_view(True, True, True)
                # print msg
            except ValueError:
                sys.stderr.write(
                    "Dado mal formatado " + str(msg) + "\n")
            except IndexError:
                sys.stderr.write("\rÍndice " + str(i) + " inexistente\n")
                pass
            except TypeError:
                print "\r No new value %s" % str(msg),
                self.stop()
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
            return ret.data


def main():
    signal.signal(signal.SIGINT, signal_handler)
    p.start()
    p.join()


if __name__ == '__main__':
    p = Plotter(f)
    p.setDaemon(True)
    main()
