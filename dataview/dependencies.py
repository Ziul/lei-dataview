#!/usr/bin/python
# -*- coding:utf-8 -*-


class Packages(object):

    """docstring for Packages"""

    def __init__(self):
        super(Packages, self).__init__()

    def list_problens(self):
        data = ''
        for p in self.__dict__.keys():
            if getattr(self, p) is False:
                data += "\t%s not installed\n" % p
        if data != '':
            data = "Problens:\n" + data
            data += "\n Install then with apt/yum"
        return data

    def __setitem__(self, key, item):
        self.__dict__[key] = item


def check():

    dependencies = Packages()

    try:
        import time
    except ImportError as e:
        dependencies[str(e).split(' ')[3]] = False
    try:
        import os
    except ImportError as e:
        dependencies[str(e).split(' ')[3]] = False
    try:
        import random
    except ImportError as e:
        dependencies[str(e).split(' ')[3]] = False
    # try:
    #     import pyqtgraph
    # except ImportError as e:
    #     dependencies['pyqtgraph'] = False
    # except Exception as e:
    #     dependencies['python-qt4'] = False
    try:
        import signal       # signals as in C
    except ImportError as e:
        dependencies[str(e).split(' ')[3]] = False
    try:
        import serial       # serial methods to read ttyUSB and semilars
    except ImportError as e:
        dependencies['python-serial'] = False
    try:
        from mock import MagicMock
    except ImportError as e:
        dependencies['mock'] = False
    try:
        import sys          # get the params
    except ImportError as e:
        dependencies[str(e).split(' ')[3]] = False

    retorno = dependencies.list_problens()
    if retorno == '':
        return True
    else:
        print(retorno)
        return False


if __name__ == '__main__':
    if check() is True:
        print("No problens found")
