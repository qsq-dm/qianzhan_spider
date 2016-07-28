# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging

# MONGO
MONGO_URI = "localhost:27017"
MONGO_DB = "qianzhan_1000"
# MONGO_NEEQ_DB = "neeq"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]


# neeq_db = mongo_client[MONGO_NEEQ_DB]
# ejinsui_db = mongo_client['ejinsui']
gaoxin_db = mongo_client['gaoxin']


class CompanyDB(object):
    def __init__(self):
        pass

    @staticmethod
    def upsert_company(item):
        logging.info("<MONGO> %s" % item)
        db.company_info_items.update({'company_name': item['company_name']}, {'$set': item}, True, True)

    @staticmethod
    def upsert_company_gaoxin(item):
        logging.info("<MONGO> %s" % item)
        db.company_info_items_gaoxin.update({'company_name': item['company_name']}, {'$set': item}, True, True)


class GaoxinDB(object):
    def __init__(self):
        pass

    @staticmethod
    def get_items():
        return gaoxin_db.company_info.find().batch_size(50)
