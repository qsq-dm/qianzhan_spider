# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests
import json
import random
import time
import urllib

from captcha import read_body_to_string

from utils import get_1000_txt


class Spider(object):
    def __init__(self):
        self._session = requests.Session()
        pass

    ''' ++++++++++login+++++++++++++++++++++'''

    def _per_login(self):
        login_page_url = "http://qiye.qianzhan.com/usercenter/login?ReturnUrl=http%3A%2F%2Fqiye.qianzhan.com%2F"
        response = self._session.get(login_page_url)
        return self._get_varifyimage(True)

    def _get_varifyimage(self, is_first=False):
        if is_first:
            varifyimage_url = "http://qiye.qianzhan.com/usercenter/varifyimage"
        else:
            varifyimage_url = "http://qiye.qianzhan.com/usercenter/varifyimage?" + str(random.random())

        response = self._session.get(varifyimage_url)
        varifycode = read_body_to_string(response.body)
        print "varifycode: %s" % varifycode.replace(' ', '')
        return varifycode

    def _do_login(self, userId, password, varifycode, max_times=10):
        form_data = {
            "userId": userId,
            "password": password,
            "VerifyCode": varifycode,
            "sevenDays": "false"
        }

        login_url = "http://qiye.qianzhan.com/usercenter/dologin"
        response = self._session.post(login_url, form_data)

        json_obj = json.loads(response.body)
        if not json_obj.get("isSuccess"):
            max_times -= 1
            if max_times > 0:
                varifycode = self._get_varifyimage(False)
                return self._do_login(userId, password, varifycode, varifycode)
            else:
                return False
        return True

    def login(self, userId, password):
        varifycode = self._per_login()
        is_success = self._do_login(userId, password, varifycode)
        # print(s.cookies.get_dict())
        return is_success

    '''++++++++++run+++++++++++++++++++++'''

    def get_searchlistview(self, search_key, page=1):
        # url = "http://www.qichacha.com/search?key=" + urllib.quote(search_key.encode('utf-8')) + "&index=0"
        # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
        #     search_key.encode('utf-8')) + "?o=0&area=0&areaN=%E5%85%A8%E5%9B%BD&p=1"
        url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
            search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC&p=" + str(page)

        response = self._session.get(url)
        print(response.text)

    def run(self):
        txt = get_1000_txt()
        for i in range(len(txt)):
            for j in range(len(txt)):
                if i >= 27 and j >= 559:
                    search_key = txt[i] + txt[j]
                    # search_key = u'一三'
                    print "++++++1000+++++++: %s %d %d %d %s" % (
                        time.strftime('%Y-%m-%d', time.localtime(time.time())), i, j, len(txt), search_key)
                    self.get_searchlistview(search_key)
