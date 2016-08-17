# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from spider import Spider
from config import userId, password, log_file1, log_file2
from log import init_logging
import logging
import time

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
print "sys default encoding: ", sys.getdefaultencoding()


def main():
    init_logging(log_file1, log_file2)
    spider = Spider(userId, password)
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    spider.run()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logging.info("begin: %s, end: %s" % (begin_time, end_time))
    pass


if __name__ == "__main__":
    main()
    pass
