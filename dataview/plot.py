#!/usr/bin/python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
from threading import Thread
from data import DataRead


class Plotter(Thread):

    """docstring for Plotter"""
    alive = False

    def __init__(self, readermethod):
        super(Plotter, self).__init__()
        self.read = readermethod
        self.name = 'Plotter'

    def start(self):
        self.alive = True
        super(Plotter, self).start()

    def stop(self):
        self.alive = False

    def run(self):
        while self.alive:
            self.read()
