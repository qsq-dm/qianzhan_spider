# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import codecs

import pymongo

# MONGO
MONGO_URI = "localhost:27017"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["qianzhan"]
db_1000 = mongo_client["qianzhan_1000"]

if __name__ == "__main__":
    cur = db_1000.company_info_items.find({}, {"_id": 0}).batch_size(50)
    for item in cur:
        db.company_info_items_detail.update({'company_name': item['company_name']}, {'$set': item}, True, True)
