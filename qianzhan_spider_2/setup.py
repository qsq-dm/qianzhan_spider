# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from spider import Spider
from config import userId, password


def main():
    spider = Spider(userId, password)
    spider.run()
    pass

if __name__ == "__main__":
    main()
    pass
