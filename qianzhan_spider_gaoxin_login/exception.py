# -*- coding:utf-8 -*-
__author__ = 'zhaojm'


class Error302(Exception):
    def __init__(self, i=0, j=0):
        self.message = "verify fail error, i: %d, j:%d" % (i, j)
        pass
