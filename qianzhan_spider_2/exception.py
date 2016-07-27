# -*- coding:utf-8 -*-
__author__ = 'zhaojm'


class VerifyFailError(Exception):
    def __init__(self):
        self.message = "verify fail error"
        pass
