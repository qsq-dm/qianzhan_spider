# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging

# MONGO
MONGO_URI = "localhost:27017"
# MONGO_NEEQ_DB = "neeq"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["qianzhan"]

import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", '127.0.0.1')
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)


class CompanyDB(object):
    def __init__(self):
        pass

    @staticmethod
    def upsert_company(item):
        logging.info("<MONGO> %s" % item)
        db.company_info_items.update({'company_name': item['company_name']}, {'$set': item}, True, True)

    @staticmethod
    def get_companys():
        return db.company_info_items.find().batch_size(50)


class RedisClient(object):
    def __init__(self):
        pass

    @staticmethod
    def set_company_name_key(company_name):
        redis_client.hset("company_name", company_name, True)

    @staticmethod
    def get_company_name_key(company_name):
        return redis_client.hexists("company_name", company_name)

    @staticmethod
    def set_company_url_key(url):
        redis_client.hset("company_url", url, True)

    @staticmethod
    def get_company_url_key(url):
        return redis_client.hget("company_url", url)


if __name__ == "__main__":

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")
    print "sys default encoding: ", sys.getdefaultencoding()


    cur = CompanyDB.get_companys()
    for company in cur:
        logging.info(company['company_name'])
        RedisClient.set_company_name_key(company['company_name'].strip())
