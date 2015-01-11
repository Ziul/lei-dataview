#!/usr/bin/python
# -*- coding:utf-8 -*-

from dataview import dependencies

if dependencies.check() is False:
    exit()
