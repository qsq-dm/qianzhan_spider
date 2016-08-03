# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import codecs

import pymongo

# MONGO
MONGO_URI = "localhost:27017"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["qianzhan"]

if __name__ == "__main__":
    cur = db.company_info_items_detail.find(
        {},
        {"_id": 0, "searchitemsite": 0, "searchitemdftz": 0, "getcommentlist": 0, "searchitemnbinfo": 0,
         "SearchItemCCXX": 0, "searchitemnb": 0}
    ).batch_size(50)
    for item in cur:
        db.company_info_items_base.update({'company_name': item['company_name']}, {'$set': item}, True, True)
