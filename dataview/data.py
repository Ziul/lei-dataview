#!/usr/bin/python
# -*- coding:utf-8 -*-

from scanf import sscanf


class DataRead(object):

    """docstring for DataRead"""
    time = ''
    data = []

    def __init__(self, arg=''):
        super(DataRead, self).__init__()
        if len(arg) > 0:
            self.read(arg)

    def setSerial(self, port):
        self.serial = port

    def __read(self):
        line = self.serial.getline()
        data = ''
        while (line != '\n'):
            data += line
        return data

    def read(self, loaded):
        self.time = sscanf(loaded, "%s\n%d %d %d\n%d %d %d\n%d %d %d\n")[0]
        self.data = sscanf(loaded, "%s\n%d %d %d\n%d %d %d\n%d %d %d\n")[1:]
        return self

    def __str__(self):
        return ("%s : " % self.time) + str(self.data)


if __name__ == '__main__':

    import sys

    data = ''
    store = []
    # store = {}
    datastore = DataRead(data)
    for line in sys.stdin:
        if line != '\n':
            data += line
        else:
            ret = datastore.read(data)
            store.append(datastore.data)
            # store[datastore.time] = datastore.data
            print ret.time
            data = ''
    # print(store)
