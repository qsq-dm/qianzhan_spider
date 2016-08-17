# -*- coding:utf-8 -*-
__author__ = 'zhaojm'


class Error302(Exception):
    def __init__(self, i=0, j=0):
        self.message = "verify fail error, i: %d, j:%d" % (i, j)
        pass


class Error403(Exception):
    def __init__(self, i=0, j=0):
        self.message = "error 403, i: %d, j:%d" % (i, j)
        pass


class Error404(Exception):
    def __init__(self, i=0, j=0):
        self.message = "error 404, i: %d, j:%d" % (i, j)
        pass


class ErrorStatusCode(Exception):
    def __init__(self, i=0, j=0):
        self.message = "error status code, i: %d, j:%d" % (i, j)
        pass
