# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging
import time

# MONGO
MONGO_URI = "localhost:27017"
mongo_client = pymongo.MongoClient(MONGO_URI)
qianzhan_db = mongo_client["qianzhan"]


class QianzhanDB(object):
    def __init__(self):
        pass

    @staticmethod
    def company_details():
        return qianzhan_db.company_info_items_detail.find().batch_size(50)

    @staticmethod
    def upsert_company_export(item):
        logging.info("<MONGO> %s" % item)
        qianzhan_db.company_info_export.update({'company_name': item['company_name']}, {'$set': item}, True, True)


if __name__ == "__main__":
    cur = QianzhanDB.company_details()
    for item in cur:
        result = {
            "company_name": item['company_name'],
            "business_address": item['business_address'],
            "business_scope": item['business_scope'],
            "business_status": item['business_status'],
            "business_type": item['business_type'],
            "legal_representative": item['legal_representative'],
            "operating_period": item['operating_period'],
            "organization_registration_code": item['organization_registration_code'],
            "province": item['province'],
            "register_date": item['register_date'],
            "registration_authority": item['registration_authority'],
            "registered_capital": item['registered_capital'],
            "registration_number": item['registration_number'],

            # "email": item['searchitemnb.nbInfo.mail'],
            # "phone": item['searchitemnb.nbInfo.phone'],

            "item_from": "qianzhan",

            "x_updatetime": 0,
            "x_status": 0,
            "x_sign": 0,
            "x_label": [],
            # "x_register_date": time.strftime("%Y%m%d", time.strptime(item['register_date'], "%Y-%m-%d")),
            "sort": 1
        }
        try:
            result.update({"email": item['searchitemnb']['nbInfo']['mail']})
        except:
            pass
        try:
            result.update({"phone": item['searchitemnb']['nbInfo']['phone']})
        except:
            pass
        try:
            result.update({
                "x_register_date": time.strftime("%Y%m%d", time.strptime(item['register_date'], "%Y-%m-%d"))
            })
        except Exception, e:
            pass

        QianzhanDB.upsert_company_export(result)
