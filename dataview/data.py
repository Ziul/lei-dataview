#!/usr/bin/python
# -*- coding:utf-8 -*-


class DataRead(object):

    """docstring for DataRead"""
    time = ''
    data = []

    def __init__(self):
        super(DataRead, self).__init__()

    def read(self, loaded):
        pass

from scanf import sscanf
import sys

data = ''
for line in sys.stdin:
    if line != '\n':
        data += line
    else:
        print "lido: \n %s" % data,
        print sscanf(data, "%s\n%d %d %d\n%d %d %d\n%d %d %d\n")
        data = ''
