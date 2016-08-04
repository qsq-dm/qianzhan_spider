# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time
import urllib
import logging
from bs4 import BeautifulSoup
from urlparse import urljoin

from utils import get_1000_txt

from mongo import QianzhanDB, GaoxinDB

from qianzhan_client import QianzhanClient
from exception import VerifyFailError

from mredis import RedisClient


class Spider(object):
    def __init__(self, userId, password):
        self._qianzhan_client = QianzhanClient(userId, password)
        pass

    def _get_company(self, url):

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

        # logging.debug("company:->%s" % company)

        company.update({'getcommentlist': self._qianzhan_client.post_getcommentlist(company['hdencryptCode'])})
        company.update({'SearchItemCCXX': self._qianzhan_client.post_SearchItemCCXX(company['hdencryptCode'],
                                                                                    company['hdoc_area'])})
        company.update({'searchitemdftz': self._qianzhan_client.post_searchitemdftz(company['company_name'])})
        company.update({'searchitemnbinfo': self._qianzhan_client.post_searchitemnbinfo(company['hdencryptCode'],
                                                                                        company['hdoc_area'])})
        if company['searchitemnbinfo'] and len(company['searchitemnbinfo']) > 0:
            company.update(
                {'searchitemnb': self._qianzhan_client.post_searchitemnb(company['hdencryptCode'], company['hdoc_area'],
                                                                         company['searchitemnbinfo'][0].get('year'))})
        company.update({'searchitemsite': self._qianzhan_client.post_searchitemsite(company['hdencryptCode'])})

        # print "company:->", company

        return company

    def _get_search(self, url):

        response = self._qianzhan_client.get_search(url)

        soup = BeautifulSoup(response.text, 'lxml')

        link_li_list = soup.select("body ul[class='list-search'] li p[class='tit'] a")
        for tag in link_li_list:
            href = tag['href']
            company_name = tag.text
            company_url = urljoin("http://qiye.qianzhan.com/", href)
            logging.info("company_name:->%s" % company_name)
            try:
                company = self._get_company(company_url)
                if company:
                    QianzhanDB.upsert_company(company)  # upsert company
                    RedisClient.set_company_name_base_key(company['company_name'])
            except VerifyFailError, err:
                logging.exception("get_company VerifyFailError, company_name:->%s, e:->%s" % (company_name, err))
                raise err
            except Exception, e:
                logging.exception("get_company exception, company_name:->%s, e:->%s" % (company_name, e))
                pass
            break
            # try:
            #     next_page_href = soup.select_one('body a[class="next"]')['href']
            # except Exception, e:
            #     next_page_href = None
            #     pass
            # if next_page_href:
            #     if next_page_href.find("http") < 0:
            #         next_page_url = urljoin("http://qiye.qianzhan.com/", next_page_href)
            #     else:
            #         next_page_url = next_page_href
            #     # print "next_page_url:->" + next_page_url
            #     self._get_search(next_page_url)

    def _run(self):
        # for i in range(len(self._txt)):
        #     for j in range(len(self._txt)):
        cur = GaoxinDB.get_items()
        for item in cur:
            # search_key = self._txt[i] + self._txt[j]
            # search_key = u'在线途游(北京)科技有限公司'
            # search_key = u'北京'
            search_key = item['company_name']
            search_key_2 = search_key.replace("（", "(").replace("）", ")")
            if RedisClient.get_company_name_detail_key(search_key_2):
                continue
            if QianzhanDB.is_had(search_key_2):
                logging.debug("has")
                continue

            if RedisClient.get_company_name_detail_key(search_key):
                continue
            if QianzhanDB.is_had(search_key):
                logging.debug("has")
                continue

            logging.info("++++++crawl gaoxin:->search_key: %s" % search_key)
            # url = "http://www.qichacha.com/search?key=" + urllib.quote(search_key.encode('utf-8')) + "&index=0"
            # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
            #     search_key.encode('utf-8')) + "?o=0&area=0&areaN=%E5%85%A8%E5%9B%BD&p=1"
            # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
            #     search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC&p=" + str(page)
            url = "http://qiye.qianzhan.com/search/qy/" + urllib.quote(
                search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC"

            try:
                self._get_search(url)
                RedisClient.set_company_name_detail_key(search_key)
            except VerifyFailError, err:
                raise VerifyFailError()
            except Exception, e:
                logging.exception(
                    "_get_search:->search_key: %s, %s" % (search_key, e.message))
                pass

    def run(self):
        logging.info("+++++++++++++run++++++++++++++++")
        try:
            is_success = self._qianzhan_client.login()
            if is_success:
                self._run()
                logging.info("++++++++++++++success finish!!!++++++++")
            else:
                raise VerifyFailError()
        except VerifyFailError, err:
            logging.error(err.message)
        except Exception, e:
            logging.exception(e.message)
            pass
