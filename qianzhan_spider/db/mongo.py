# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo

# MONGO
MONGO_URI = "localhost:27017"
MONGO_DB = "qianzhan"
# MONGO_NEEQ_DB = "neeq"



mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
# neeq_db = mongo_client[MONGO_NEEQ_DB]
# ejinsui_db = mongo_client['ejinsui']
# gaoxin_db = mongo_client['gaoxin']


class CompanyInfoItemsDB(object):
    def __init__(self):
        pass

    @staticmethod
    def upsert_company_info_item(item):
        db.company_info_items.update(
            {'company_name': item['company_name']},
            {'$set': item}, True, True)

    @staticmethod
    def upsert_ejinsui(item):
        db.company_info_items_ejinsui.update(
            {'company_name': item['company_name']},
            {'$set': item}, True, True)

    @staticmethod
    def upsert_gaoxin(item):
        db.company_info_items_gaoxin.update(
            {'company_name': item['company_name']},
            {'$set': item}, True, True)


# class NeeqItemsDB(object):
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def insert_item(item):
#         # print item
#         neeq_db.neeq_items.insert(item)
#
#     @staticmethod
#     def get_neeq_items():
#         return neeq_db.neeq_items.find().batch_size(50)

class EjinsuiDB(object):
    def __init__(self):
        pass

    @staticmethod
    def get_items():
        return ejinsui_db.company_info.find().batch_size(50)


class GaoxinDB(object):
    def __init__(self):
        pass

    @staticmethod
    def get_items():
        return gaoxin_db.company_info.find().batch_size(50)
