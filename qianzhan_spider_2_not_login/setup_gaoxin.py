# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from spider_gaoxin import SpiderGaoxin
from config import userId, password
from log import init_logging

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
print "sys default encoding: ", sys.getdefaultencoding()


def main():
    init_logging("log/gaoxin.log", "log/gaoxin_spider.log")
    spider = SpiderGaoxin(userId, password)
    spider.run()
    pass


if __name__ == "__main__":
    main()
    pass
