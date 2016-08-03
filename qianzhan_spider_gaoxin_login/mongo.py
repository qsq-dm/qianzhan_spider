# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging

# MONGO
MONGO_URI = "localhost:27017"
# MONGO_NEEQ_DB = "neeq"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["qianzhan"]

gaoxin_db = mongo_client['gaoxin']
proxy_db = mongo_client['proxy']


class QianzhanDB(object):
    def __init__(self):
        pass

    @staticmethod
    def upsert_company(item):
        logging.info("<MONGO> %s" % item)
        db.company_info_items_detail.update({'company_name': item['company_name']}, {'$set': item}, True, True)


class GaoxinDB(object):
    def __init__(self):
        pass

    @staticmethod
    def get_items():
        return gaoxin_db.company_info.find().batch_size(50).skip(8884)


class ProxyDB(object):
    def __init__(self):
        pass

    @staticmethod
    def get_items():
        return proxy_db.proxy_items.find().batch_size(50)
