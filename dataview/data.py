#!/usr/bin/python
# -*- coding:utf-8 -*-

from scanf import sscanf, IncompleteCaptureError


class DataRead(object):

    """docstring for DataRead"""
    time = ''
    data = []
    formatter = "%s\n%d %d %d\n%d %d %d\n%d %d %d\n"

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
        try:
            self.time = sscanf(loaded, self.formatter)[0]
            self.data = list(sscanf(loaded, self.formatter)[1:])
            # self.time = loaded.split('\n')[0]
            # self.data = ' '.join(loaded.split('\n')[1:]).split(' ')
            self.data.remove('')
        except IncompleteCaptureError as e:
            print str(e)
        except ValueError:
            pass
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
