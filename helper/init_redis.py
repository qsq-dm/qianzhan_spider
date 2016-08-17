# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging
import redis
import os

# MONGO
MONGO_URI = "localhost:27017"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["qianzhan"]

REDIS_HOST = os.getenv("REDIS_HOST", '127.0.0.1')
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)


class QianzhanDB(object):
    def __init__(self):
        pass

    @staticmethod
    def get_companys_base():
        return db.company_info_items_base.find().batch_size(50)

    @staticmethod
    def get_companys_detail():
        return db.company_info_items_detail.find().batch_size(50)


class RedisClient(object):
    def __init__(self):
        pass

    @staticmethod
    def set_company_name_base_key(company_name):
        redis_client.hset("company_name_base", company_name, True)

    @staticmethod
    def get_company_name_base_key(company_name):
        return redis_client.hexists("company_name_base", company_name)

    @staticmethod
    def set_company_url_base_key(url):
        redis_client.hset("company_url_base", url, True)

    @staticmethod
    def get_company_url_base_key(url):
        return redis_client.hget("company_url_base", url)

    @staticmethod
    def set_company_name_detail_key(company_name):
        redis_client.hset("company_name_detail", company_name, True)

    @staticmethod
    def get_company_name_detail_key(company_name):
        return redis_client.hexists("company_name_detail", company_name)

    @staticmethod
    def set_company_url_detail_key(url):
        redis_client.hset("company_url_detail", url, True)

    @staticmethod
    def get_company_url_detail_key(url):
        return redis_client.hget("company_url_detail", url)


if __name__ == "__main__":

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")
    print "sys default encoding: ", sys.getdefaultencoding()

    # cur = QianzhanDB.get_companys_base()
    # for company in cur:
    #     logging.info(company['company_name'])
    #     RedisClient.set_company_name_base_key(company['company_name'])

    cur = QianzhanDB.get_companys_detail()
    for company in cur:
        logging.info(company['company_name'])
        RedisClient.set_company_name_detail_key(company['company_name'])
