# -*- coding:utf-8 -*-
__author__ = 'zhaojm'


import json
import random
import time
import urllib
from bs4 import BeautifulSoup
from urlparse import urljoin

from captcha import read_body_to_string

from utils import get_1000_txt

from mongo import CompanyDB

# from http_client import HTTPClient
from qianzhan_client import QianzhanClient


class Spider(object):
    def __init__(self, userId, password):
        # self._http_client = HTTPClient()
        self._userId = userId
        self._password = password
        self._qianzhan_client = QianzhanClient()
        self._company_detail_url_list = []
        self._txt = get_1000_txt()
        # self._txt_len = len(self._txt)
        # self._i = 0
        # self._j = 0
        print "txt len:->", len(self._txt)
        pass

    def login(self):
        return self._qianzhan_client.login(self._userId, self._password)

    def get_company(self, url):
        print "get_company:->", url

        if url in self._company_detail_url_list:
            return
        else:
            self._company_detail_url_list.append(url)

        response = self._qianzhan_client.get_company(url)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')

        company = {}
        company.update({'company_name': soup.select_one('h1[class="ct_name"]').contents[0]})
        try:
            company.update({'url': soup.select_one('a[class="url"]').text})
        except Exception, e:
            pass
        company.update({'item_update_time': time.strftime('%Y-%m-%d', time.localtime(time.time()))})

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
        company.update({
            'hdencryptCode': soup.select_one('input[id="hdencryptCode"]')['value'],
            'hdoc_area': soup.select_one('input[id="hdoc_area"]')['value']
        })

        print "company:->", company

        company.update({'getcommentlist': self._qianzhan_client.get_getcommentlist(company['hdencryptCode'])})
        company.update({'SearchItemCCXX': self._qianzhan_client.get_SearchItemCCXX(company['hdencryptCode'],
                                                                                   company['hdoc_area'])})
        company.update({'searchitemdftz': self._qianzhan_client.get_searchitemdftz(company['company_name'])})
        company.update({'searchitemnbinfo': self._qianzhan_client.get_searchitemnbinfo(company['hdencryptCode'],
                                                                                       company['hdoc_area'])})
        if company['searchitemnbinfo'] and len(company['searchitemnbinfo']) > 0:
            company.update(
                {'searchitemnb': self._qianzhan_client.get_searchitemnb(company['hdencryptCode'], company['hdoc_area'],
                                                                        company['searchitemnbinfo'][0].get('year'))})
        company.update({'searchitemsite': self._qianzhan_client.get_searchitemsite(company['hdencryptCode'])})

        # print "company:->", company

        return company

    def get_search(self, search_key):

        response = self._qianzhan_client.get_search(search_key)
        # print(response.text)

        if response.status_code == 302:
            location = response.headers['Location']
            isSuccess = self._qianzhan_client.do_verify(location)
            if not isSuccess:
                print "++++++++do verify not success+++++++++"
                print "...run again............."
                isSuccess = self.login()
                if isSuccess:
                    print "********************"
                    print "login success!"
                    print "********************"
                    self.get_search(search_key)
                else:
                    print "********************"
                    print "login error......."
                    print "********************"
                    pass
                return
            else:
                self.get_search(search_key)

        soup = BeautifulSoup(response.text, 'lxml')

        link_li_list = soup.select("body ul[class='list-search'] li p[class='tit'] a")
        for tag in link_li_list:
            href = tag['href']
            company_name = tag.text
            company_url = urljoin("http://qiye.qianzhan.com/", href)
            print "company_name:->", company_name
            print "company_url:->" + company_url
            try:
                company = self.get_company(company_url)
                CompanyDB.upsert_company(company)  # upsert company
            except Exception, e:
                print "get_company exception, company_name:->", company_name
                print e
                pass
        try:
            next_page_href = soup.select_one('body a[class="next"]')['href']
        except Exception, e:
            next_page_href = None
            pass
        if next_page_href:
            next_page_url = urljoin("http://qiye.qianzhan.com/", next_page_href)
            print "next_page_url:->" + next_page_url
            self.get_search(next_page_url)

    def _run(self):
        for i in range(len(self._txt)):
            for j in range(len(self._txt)):
                search_key = self._txt[i] + self._txt[j]
                # search_key = u'在线途游(北京)科技有限公司'
                # search_key = u'北京'
                print "++++++1000+++++++: %s %d %d %d %s" % (
                    time.strftime('%Y-%m-%d', time.localtime(time.time())), i, j, len(self._txt), search_key)

                self.get_search(search_key)


    def run(self):
        print "+++++++++++++run++++++++++++++++"

        isSuccess = self.login()
        if isSuccess:
            print "********************"
            print "login success!"
            print "********************"

            self._run()
        else:
            print "********************"
            print "login error......."
            print "********************"
            pass
