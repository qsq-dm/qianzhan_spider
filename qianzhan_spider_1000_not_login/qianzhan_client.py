# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import random
import time
import logging
from urlparse import urljoin
from captcha import read_body_to_string
from http_client import HTTPClient

from exception import VerifyFailError, Error403


class QianzhanClient(object):
    def __init__(self, userId, password):
        self._userId = userId
        self._password = password
        self._http_client = HTTPClient()
        pass

    """+++++++++++++++++++login++++++++++++"""

    # def _per_login(self):
    #     login_page_url = "http://qiye.qianzhan.com/usercenter/login?ReturnUrl=http%3A%2F%2Fqiye.qianzhan.com%2F"
    #     response = self._http_client.get(login_page_url)
    #     return self._get_varifyimage(True)

    def _get_varifyimage(self, is_first=False):
        if is_first:
            varifyimage_url = "http://qiye.qianzhan.com/usercenter/varifyimage"
        else:
            varifyimage_url = "http://qiye.qianzhan.com/usercenter/varifyimage?" + str(random.random())

        response = self._http_client.get(varifyimage_url)
        varifycode = read_body_to_string(response.content)
        logging.debug("varifycode: %s" % varifycode.replace(' ', ''))
        return varifycode.replace(' ', '')

    # def _do_login(self, varifycode, max_times=10):
    #     form_data = {
    #         "userId": self._userId,
    #         "password": self._password,
    #         "VerifyCode": varifycode,
    #         "sevenDays": "false"
    #     }
    #     login_url = "http://qiye.qianzhan.com/usercenter/dologin"
    #     response = self._http_client.post(login_url, form_data)
    #     json_obj = response.json()
    #
    #     logging.debug("sMsg: %s" % json_obj.get("sMsg"))
    #
    #     if not json_obj.get("isSuccess"):
    #         # print json_obj.get("sMsg")
    #         max_times -= 1
    #         if max_times > 0:
    #             varifycode = self._get_varifyimage()
    #             return self._do_login(varifycode, max_times)
    #         else:
    #             return False
    #     # print json_obj.get("sMsg")
    #     logging.info("cookie: %s" % response.cookies.get_dict())
    #     return True

    # def login(self):
    #     # print "++++++++++++++login+++++++++++++++++"
    #     varifycode = self._per_login()
    #     is_success = self._do_login(varifycode)
    #     return is_success

    '''++++++++++++++++++userverify+++++++++++++++++++'''

    def _pre_varify(self, url):
        try:
            response = self._http_client.get(url)
        except Exception, e:
            pass
        return self._get_varifyimage()

    def _do_verify(self, varifycode, max_times=10):
        # form_data = {
        #     "VerifyCode": varifycode.replace(' ', ''),
        #     "sevenDays": "false"
        # }
        check_varify_image_url = "http://qiye.qianzhan.com/usercenter/CheckVarifyImage?VerifyCode=" + varifycode
        response = self._http_client.post(check_varify_image_url)
        json_obj = response.json()

        if not json_obj.get("isSuccess"):
            max_times -= 1
            if max_times > 0:
                varifycode = self._get_varifyimage()
                self._do_verify(varifycode, max_times)
            else:
                return False
        return True

    def do_verify(self, url):
        # print "++++++++++++++do_verify+++++++++++++++++"
        varifycode = self._pre_varify(url)
        is_success = self._do_verify(varifycode)
        return is_success

    """+++++++++++verify post get++++++++"""

    def _verify_post(self, url, data=None, json=None, **kwargs):
        kwargs.setdefault("allow_redirects", False)
        response = self._http_client.post(url, data, json, **kwargs)
        if response.status_code == 302:
            location = response.headers['Location']
            user_verify_url = urljoin("http://qiye.qianzhan.com/", location)
            is_success = self.do_verify(user_verify_url)
            if is_success:
                response = self._verify_post(url, data, json, **kwargs)
            else:
                # is_success = self.login()
                # if is_success:
                #     response = self._http_client.post(url, data, json, **kwargs)
                # else:
                raise VerifyFailError()
        elif response.status_code == 403:
            raise Error403()
        return response

    def _verify_get(self, url, **kwargs):
        kwargs.setdefault("allow_redirects", False)
        response = self._http_client.get(url, **kwargs)
        if response.status_code == 302:
            location = response.headers['Location']
            user_verify_url = urljoin("http://qiye.qianzhan.com/", location)
            is_success = self.do_verify(user_verify_url)
            if is_success:
                response = self._verify_get(url, **kwargs)
            else:
                # is_success = self.login()
                # if is_success:
                #     response = self._http_client.get(url, **kwargs)
                # else:
                raise VerifyFailError()
        elif response.status_code == 403:
            raise Error403()
        return response

    """""+++++++++++++++hehe+++++++++++++++++++"""

    # def post_getcommentlist(self, hdencryptCode):
    #     url = "http://qiye.qianzhan.com/orgcompany/getcommentlist"
    #     form_data = {
    #         'orgCode': hdencryptCode,
    #         'page': '1',
    #         'pagesize': '5'
    #     }
    #     response = self._verify_post(url, form_data)
    #     json_obj = response.json()
    #     # logging.debug("sMsg: %s" % json_obj.get("sMsg"))
    #     # logging.debug("getcommentlist:->%s" % json_obj)
    #
    #     if json_obj.get("isSuccess"):
    #         dataList = json_obj.get('dataList')
    #     else:
    #         dataList = None
    #         # print json_obj.get("sMsg")
    #     return dataList

    # def post_SearchItemCCXX(self, hdencryptCode, hdoc_area):
    #     url = "http://qiye.qianzhan.com/orgcompany/SearchItemCCXX"
    #     form_data = {
    #         'orgCode': hdencryptCode,
    #         'oc_area': hdoc_area
    #     }
    #     response = self._verify_post(url, form_data)
    #
    #     json_obj = response.json()
    #     # logging.debug("sMsg: %s" % json_obj.get("sMsg"))
    #     # print "SearchItemCCXX:->", json_obj
    #
    #     if json_obj.get("isSuccess"):
    #         dataList = json_obj.get('dataList')
    #     else:
    #         dataList = None
    #         # print json_obj.get("sMsg")
    #     return dataList

    # def post_searchitemdftz(self, company_name):
    #     url = "http://qiye.qianzhan.com/orgcompany/searchitemdftz"
    #     form_data = {
    #         'orgName': company_name,
    #         'page': '1',
    #         'pagesize': '10'
    #     }
    #     response = self._verify_post(url, form_data)
    #     json_obj = response.json()
    #     # print "searchitemdftz:->", json_obj
    #
    #     if json_obj.get("isSuccess"):
    #         dataList = json_obj.get('dataList')
    #     else:
    #         dataList = None
    #         # print json_obj.get("sMsg")
    #     return dataList

    # def post_searchitemnbinfo(self, hdencryptCode, hdoc_area):
    #     url = "http://qiye.qianzhan.com/orgcompany/searchitemnbinfo"
    #     form_data = {
    #         'orgCode': hdencryptCode,
    #         'areaCode': hdoc_area
    #     }
    #     response = self._verify_post(url, form_data)
    #     json_obj = response.json()
    #     # print "searchitemnbinfo:->", json_obj
    #
    #     if json_obj.get("isSuccess"):
    #         dataList = json_obj.get('dataList')
    #     else:
    #         dataList = None
    #         # print json_obj.get("sMsg")
    #
    #     if isinstance(dataList, dict):
    #         dataList = [dataList]
    #
    #     return dataList

    # def post_searchitemnb(self, hdencryptCode, hdoc_area, year):
    #
    #     url = "http://qiye.qianzhan.com/orgcompany/searchitemnb"
    #     form_data = {
    #         'orgCode': hdencryptCode,
    #         'areaCode': hdoc_area,
    #         'year': str(year),
    #     }
    #     response = self._verify_post(url, form_data)
    #     json_obj = response.json()
    #     # print "searchitemnb:->", json_obj
    #
    #     if json_obj.get("isSuccess"):
    #         dataList = json_obj.get('dataList')
    #     else:
    #         dataList = None
    #         # print json_obj.get("sMsg")
    #     return dataList

    # def post_searchitemsite(self, hdencryptCode):
    #
    #     url = "http://qiye.qianzhan.com/orgcompany/searchitemsite"
    #     form_data = {
    #         'orgCode': hdencryptCode,
    #         'page': '1',
    #         'pagesize': '10'
    #     }
    #     response = self._verify_post(url, form_data)
    #
    #     json_obj = response.json()
    #     # print "searchitemsite:->", json_obj
    #
    #     if json_obj.get("isSuccess"):
    #         dataList = json_obj.get('dataList')
    #     else:
    #         dataList = None
    #         # print json_obj.get("sMsg")
    #     return dataList

    def get_company(self, url):
        response = self._verify_get(url)
        return response

    def get_search(self, url):
        response = self._verify_get(url)
        return response
