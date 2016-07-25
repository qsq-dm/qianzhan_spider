# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import codecs

import pymongo

# MONGO
MONGO_URI = "localhost:27017"
MONGO_DB = "gaoxin"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
print "sys default encoding: ", sys.getdefaultencoding()



def upsert_company_info_item(item):
    db.company_info.update(
        {'company_name': item['company_name']},
        {'$set': item}, True, True)


if __name__ == "__main__":
    f = codecs.open('data/gaoxin.txt', 'r', 'utf-8')
    for line in f.readlines():
        line = line.strip()
        if line:
            upsert_company_info_item({"company_name": line})
            # print line
