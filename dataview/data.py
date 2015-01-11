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

    def read(self, loaded):
        self.time = sscanf(loaded, "%s\n%d %d %d\n%d %d %d\n%d %d %d\n")[0]
        self.data = sscanf(loaded, "%s\n%d %d %d\n%d %d %d\n%d %d %d\n")[1:]


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
            datastore.read(data)
            store.append(datastore.data)
            # store[datastore.time] = datastore.data
            data = ''
    print(store)
