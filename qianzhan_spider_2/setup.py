# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from spider import Spider
from config import userId, password


def main():
    # try:
    spider = Spider(userId, password)
    spider.run()

    # except Exception, e:
    #     print "main:->Exception->" + e.message
    pass


if __name__ == "__main__":
    main()
    pass
