# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo

# MONGO
MONGO_URI = "localhost:27017"
MONGO_DB = "qianzhan_1000"
# MONGO_NEEQ_DB = "neeq"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]


# neeq_db = mongo_client[MONGO_NEEQ_DB]
# ejinsui_db = mongo_client['ejinsui']
# gaoxin_db = mongo_client['gaoxin']


class CompanyDB(object):
    def __init__(self):
        pass

    @staticmethod
    def upsert_company(item):
        print "upsert:->", item
        db.company_info_items.update({'company_name': item['company_name']}, {'$set': item}, True, True)
