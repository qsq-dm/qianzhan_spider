# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import random
import time
import urllib
from captcha import read_body_to_string
from http_client import HTTPClient


class QianzhanClient(object):
    def __init__(self):
        self._http_client = HTTPClient()
        pass

    ''' ++++++++++login+++++++++++++++++++++'''

    def _per_login(self):
        login_page_url = "http://qiye.qianzhan.com/usercenter/login?ReturnUrl=http%3A%2F%2Fqiye.qianzhan.com%2F"
        response = self._http_client.get(login_page_url)
        return self._get_varifyimage(True)

    def _get_varifyimage(self, is_first=False):
        if is_first:
            varifyimage_url = "http://qiye.qianzhan.com/usercenter/varifyimage"
        else:
            varifyimage_url = "http://qiye.qianzhan.com/usercenter/varifyimage?" + str(random.random())

        response = self._http_client.get(varifyimage_url)
        varifycode = read_body_to_string(response.content)
        print "varifycode: %s" % varifycode.replace(' ', '')
        return varifycode.replace(' ', '')

    def _do_login(self, userId, password, varifycode, max_times=10):
        form_data = {
            "userId": userId,
            "password": password,
            "VerifyCode": varifycode,
            "sevenDays": "false"
        }

        login_url = "http://qiye.qianzhan.com/usercenter/dologin"
        response = self._http_client.post(login_url, form_data)
        json_obj = response.json()
        # print json_obj
        if not json_obj.get("isSuccess"):
            print json_obj.get("sMsg")
            max_times -= 1
            if max_times > 0:
                varifycode = self._get_varifyimage()
                return self._do_login(userId, password, varifycode, max_times)
            else:
                return False
        print json_obj.get("sMsg")
        print "cookie:->", response.cookies.get_dict()
        return True

    def login(self, userId, password):
        varifycode = self._per_login()
        is_success = self._do_login(userId, password, varifycode)
        return is_success

    '''++++++++++company+++++++++++++++++++++'''

    def get_getcommentlist(self, hdencryptCode):
        url = "http://qiye.qianzhan.com/orgcompany/getcommentlist"
        form_data = {
            'orgCode': hdencryptCode,
            'page': '1',
            'pagesize': '5'
        }
        response = self._http_client.post(url, form_data)
        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "getcommentlist:->", json_obj

        if json_obj.get("isSuccess"):
            dataList = json_obj.get('dataList')
        else:
            dataList = None
            print json_obj.get("sMsg")
        return dataList

    def get_SearchItemCCXX(self, hdencryptCode, hdoc_area):
        url = "http://qiye.qianzhan.com/orgcompany/SearchItemCCXX"
        form_data = {
            'orgCode': hdencryptCode,
            'oc_area': hdoc_area
        }
        response = self._http_client.post(url, form_data)

        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "SearchItemCCXX:->", json_obj

        if json_obj.get("isSuccess"):
            dataList = json_obj.get('dataList')
        else:
            dataList = None
            print json_obj.get("sMsg")
        return dataList

    def get_searchitemdftz(self, company_name):
        url = "http://qiye.qianzhan.com/orgcompany/searchitemdftz"
        form_data = {
            'orgName': company_name,
            'page': '1',
            'pagesize': '10'
        }
        response = self._http_client.post(url, form_data)

        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "searchitemdftz:->", json_obj

        if json_obj.get("isSuccess"):
            dataList = json_obj.get('dataList')
        else:
            dataList = None
            print json_obj.get("sMsg")
        return dataList

    def get_searchitemnbinfo(self, hdencryptCode, hdoc_area):
        url = "http://qiye.qianzhan.com/orgcompany/searchitemnbinfo"
        form_data = {
            'orgCode': hdencryptCode,
            'areaCode': hdoc_area
        }
        response = self._http_client.post(url, form_data)
        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "searchitemnbinfo:->", json_obj

        if json_obj.get("isSuccess"):
            dataList = json_obj.get('dataList')
        else:
            dataList = None
            print json_obj.get("sMsg")

        if isinstance(dataList, dict):
            dataList = [dataList]

        return dataList

    def get_searchitemnb(self, hdencryptCode, hdoc_area, year):
        # print "searchitemnbinfo: ", dataList

        print "+++++++++dataList is not empty+++++++++++"
        # print type(dataList)
        # print dataList
        # print dataList[0]
        url = "http://qiye.qianzhan.com/orgcompany/searchitemnb"
        form_data = {
            'orgCode': hdencryptCode,
            'areaCode': hdoc_area,
            'year': str(year),
        }
        response = self._http_client.post(url, form_data)
        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "searchitemnb:->", json_obj

        if json_obj.get("isSuccess"):
            dataList = json_obj.get('dataList')
        else:
            dataList = None
            print json_obj.get("sMsg")
        return dataList

    def get_searchitemsite(self, hdencryptCode):

        url = "http://qiye.qianzhan.com/orgcompany/searchitemsite"
        form_data = {
            'orgCode': hdencryptCode,
            'page': '1',
            'pagesize': '10'
        }
        response = self._http_client.post(url, form_data)
        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "searchitemsite:->", json_obj

        if json_obj.get("isSuccess"):
            dataList = json_obj.get('dataList')
        else:
            dataList = None
            print json_obj.get("sMsg")
        return dataList

    '''++++++++++++++++++userverify+++++++++++++++++++'''

    def _pre_varify(self, url):
        response = self._http_client.get(url)
        return self._get_varifyimage()

    def _do_verify(self, varifycode, max_times=10):
        # form_data = {
        #     "VerifyCode": varifycode.replace(' ', ''),
        #     "sevenDays": "false"
        # }
        check_varify_image_url = "http://qiye.qianzhan.com/usercenter/CheckVarifyImage?VerifyCode=" + varifycode.replace(
            ' ', '')
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
        print "do_verify:->", url
        varifycode = self._pre_varify(url)
        is_success = self._do_verify(varifycode)
        return is_success

    def get_company(self, url):
        return self._http_client.get(url)

    def get_search(self, search_key):
        # url = "http://www.qichacha.com/search?key=" + urllib.quote(search_key.encode('utf-8')) + "&index=0"
        # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
        #     search_key.encode('utf-8')) + "?o=0&area=0&areaN=%E5%85%A8%E5%9B%BD&p=1"
        # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
        #     search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC&p=" + str(page)
        url = "http://qiye.qianzhan.com/search/qy/" + urllib.quote(
            search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC"
        return self._http_client.get(url, allow_redirects=False)
