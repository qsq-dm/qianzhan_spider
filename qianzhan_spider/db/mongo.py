# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo

from qianzhan_spider.settings import MONGO_URI, MONGO_DB, MONGO_NEEQ_DB

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
neeq_db = mongo_client[MONGO_NEEQ_DB]


class CompanyInfoItemsDB(object):
    def __init__(self):
        pass

    @staticmethod
    def upsert_company_info_item(item):
        db.company_info_items.update(
            {'company_name': item['company_name']},
            {'$set': item}, True, True)


class NeeqItemsDB(object):
    def __init__(self):
        pass

    @staticmethod
    def insert_item(item):
        # print item
        neeq_db.neeq_items.insert(item)

    @staticmethod
    def get_neeq_items():
        return neeq_db.neeq_items.find().batch_size(50)
