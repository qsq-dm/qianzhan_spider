# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging
import time

# MONGO
# MONGO_URI = "localhost:27017"
MONGO_URI = 'mongodb://supeiyunjing:spyj2016@localhost:27017'
mongo_client = pymongo.MongoClient(MONGO_URI)
spyj_db = mongo_client["spyj"]


class QianzhanDB(object):
    def __init__(self):
        pass

    @staticmethod
    def company_tmp():
        return spyj_db.tmp.find({}, {"_id": 0}).batch_size(50)

    @staticmethod
    def upsert_company_info(item):
        logging.info("<MONGO> %s" % item)
        spyj_db.company_info.update({'company_name': item['company_name']}, {'$set': item}, True, True)


if __name__ == "__main__":
    cur = QianzhanDB.company_tmp()
    for item in cur:
        # print item
        QianzhanDB.upsert_company_info(item)
