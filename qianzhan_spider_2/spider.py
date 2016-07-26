# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests
import json
import random
import time
import urllib
from bs4 import BeautifulSoup
from urlparse import urljoin

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
        varifycode = read_body_to_string(response.content)
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

        json_obj = response.json()
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

    '''++++++++++company+++++++++++++++++++++'''

    def get_getcommentlist(self, hdencryptCode):
        url = "http://qiye.qianzhan.com/orgcompany/getcommentlist"
        form_data = {
            'orgCode': hdencryptCode,
            'page': '1',
            'pagesize': '5'
        }
        response = self._session.post(url=url, formdata=form_data)
        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "getcommentlist:->", json_obj
        dataList = json_obj['dataList']
        return dataList

    def get_SearchItemCCXX(self, hdencryptCode, hdoc_area):
        url = "http://qiye.qianzhan.com/orgcompany/SearchItemCCXX"
        form_data = {
            'orgCode': hdencryptCode,
            'areaCode': hdoc_area
        }
        response = self._session.post(url=url, formdata=form_data)

        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "SearchItemCCXX:->", json_obj
        dataList = json_obj['dataList']
        return dataList

    def get_searchitemdftz(self, company_name):
        url = "http://qiye.qianzhan.com/orgcompany/searchitemdftz"
        form_data = {
            'orgName': company_name,
            'page': '1',
            'pagesize': '10'
        }
        response = self._session.post(url=url, formdata=form_data)

        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "searchitemdftz:->", json_obj
        dataList = json_obj['dataList']
        return dataList

    def get_searchitemnbinfo(self, hdencryptCode, hdoc_area):
        url = "http://qiye.qianzhan.com/orgcompany/searchitemnbinfo"
        form_data = {
            'orgCode': hdencryptCode,
            'areaCode': hdoc_area
        }
        response = self._session.post(url=url, formdata=form_data)
        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "searchitemnbinfo:->", json_obj
        dataList = json_obj['dataList']

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
        response = self._session.post(url=url, formdata=form_data)
        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "searchitemnb:->", json_obj
        dataList = json_obj['dataList']
        return dataList

    def get_searchitemsite(self, hdencryptCode):

        url = "http://qiye.qianzhan.com/orgcompany/searchitemsite"
        form_data = {
            'orgCode': hdencryptCode,
            'page': '1',
            'pagesize': '10'
        }
        response = self._session.post(url=url, formdata=form_data)
        json_obj = response.json()
        # json_obj = json.loads(json_text)
        print "searchitemsite:->", json_obj
        dataList = json_obj['dataList']
        return dataList

    def get_company(self, url):
        response = self._session.get(url)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')

        company = {}
        company.update({
            'company_name': soup.select_one('h1[class="ct_name"]').contents[0],
            'url': soup.select_one('a[class="url"]').text,
            'item_update_time': time.strftime('%Y-%m-%d', time.localtime(time.time()))
        })

        span_list = soup.select('ul[class="art-basic"] li span[class="info"]')

        company.update({
            'organization_registration_code': span_list[0].text,
            'registration_number': span_list[1].text,
            'legal_representative': span_list[2].text,
            'business_status': span_list[3].text,
            'registered_capital': span_list[4].text,
            'business_type': span_list[5].text,
            'register_date': span_list[6].text,
            'operating_period': span_list[7].text,
            'business_address': span_list[8].text,
            'business_scope': span_list[9].text
        })

        span_list_2 = soup.select('ul[class="art-org"] li span[class=""info]')

        company.update({
            'province': span_list_2[1].text,
            'registration_authority': span_list_2[4].text
        })

        # use
        company['hdencryptCode'] = soup.select_one('input[id="hdencryptCode"]')['value']
        company['hdoc_area'] = soup.select_one('input[id="hdoc_area"]')['value']

        company['getcommentlist'] = self.get_getcommentlist(company['hdencryptCode'])
        company['SearchItemCCXX'] = self.get_SearchItemCCXX(company['hdencryptCode'], company['hdoc_area'])
        company['searchitemdftz'] = self.get_searchitemdftz(company['company_name'])
        company['searchitemnbinfo'] = self.get_searchitemnbinfo(company['hdencryptCode'], company['hdoc_area'])
        if company['searchitemnbinfo'] and len(company['searchitemnbinfo']) > 0:
            company['searchitemnb'] = self.get_searchitemnb(company['hdencryptCode'], company['hdoc_area'],
                                                            company['searchitemnbinfo'][0].get('year'))
        company['searchitemsite'] = self.get_searchitemsite(company['hdencryptCode'])

        print "company:->", company

        return company

    '''++++++++++++++++++list+++++++++++++++++++'''

    def get_search(self, url):

        response = self._session.get(url)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')

        link_li_list = soup.select("body ul[class='list-search'] li p[class='tit'] a")
        for tag in link_li_list:
            href = tag['href']
            company_url = urljoin("http://qiye.qianzhan.com/", href)
            print "company_url:->" + company_url
            company = self.get_company(company_url)

        next_page_href = soup.select_one('body a[class="next"]')['href']
        if next_page_href:
            next_page_url = urljoin("http://qiye.qianzhan.com/", next_page_href)
            print "next_page_url:->" + next_page_url
            self.get_search(next_page_url)

    '''++++++++++++++++++run+++++++++++++++++++'''
    def run(self):
        txt = get_1000_txt()
        for i in range(len(txt)):
            for j in range(len(txt)):
                if i >= 27 and j >= 559:
                    search_key = txt[i] + txt[j]
                    # search_key = u'一三'
                    print "++++++1000+++++++: %s %d %d %d %s" % (
                        time.strftime('%Y-%m-%d', time.localtime(time.time())), i, j, len(txt), search_key)
                    # url = "http://www.qichacha.com/search?key=" + urllib.quote(search_key.encode('utf-8')) + "&index=0"
                    # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
                    #     search_key.encode('utf-8')) + "?o=0&area=0&areaN=%E5%85%A8%E5%9B%BD&p=1"
                    # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
                    #     search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC&p=" + str(page)
                    url = "http://qiye.qianzhan.com/search/qy/" + urllib.quote(
                        search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC&p=1"

                    self.get_search(url)
