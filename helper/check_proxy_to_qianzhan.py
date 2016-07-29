# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests

import pymongo
import time
import logging

# MONGO
MONGO_URI = "localhost:27017"
MONGO_PROXY_DB = "proxy"

mongo_client = pymongo.MongoClient(MONGO_URI)
proxy_db = mongo_client[MONGO_PROXY_DB]

if __name__ == "__main__":

    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })

    format_str = '%(asctime)s %(filename)s[line:%(lineno)d] <%(levelname)s> %(message)s'

    logging.basicConfig(
        level=logging.DEBUG,
        format=format_str,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename="log/check_proxy_to_qianzhan.log",
        filemode='w'
    )

    cur = proxy_db.proxy_items.find({}, {'_id': 0}).batch_size(50)
    for item in cur:
        time.sleep(0.3)
        logging.info("%s:%s" % (item['ip'], item['port']))
        proxies = {"http": "http://%s:%s" % (item['ip'], item['port'])}
        try:
            response = session.get("http://qiye.qianzhan.com/", proxies=proxies, timeout=2)
            logging.info("<response %d>" % response.status_code)
            if response.status_code == 200:
                proxy_db.proxy_items_qianzhan.update({"ip": item['ip'], "port": item['port']}, item, True, True)
        except Exception, e:
            logging.exception(e)
