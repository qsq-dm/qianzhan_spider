# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo

from qianzhan_spider.settings import MONGO_URI, MONGO_DB

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]


class CompanyInfoItemsDB(object):
    def __init__(self):
        pass

    @staticmethod
    def upsert_company_info_item(item):
        db.company_info_items.update(
            {'company_name': item['company_name']},
            {'$set': item}, True, True)
