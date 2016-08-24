# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time
import urllib
import logging
from bs4 import BeautifulSoup
from urlparse import urljoin

from mongo import QianzhanDB, ChinabiddingDB
from qianzhan_client import QianzhanClient
from exception import Error302, Error403, Error400, Error404
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

        # company.update({'getcommentlist': self._qianzhan_client.post_getcommentlist(company['hdencryptCode'])})
        # company.update({'SearchItemCCXX': self._qianzhan_client.post_SearchItemCCXX(company['hdencryptCode'],
        #                                                                             company['hdoc_area'])})
        # company.update({'searchitemdftz': self._qianzhan_client.post_searchitemdftz(company['company_name'])})
        company.update({'searchitemnbinfo': self._qianzhan_client.post_searchitemnbinfo(company['hdencryptCode'],
                                                                                        company['hdoc_area'])})
        if company['searchitemnbinfo'] and len(company['searchitemnbinfo']) > 0:
            company.update(
                {'searchitemnb': self._qianzhan_client.post_searchitemnb(company['hdencryptCode'], company['hdoc_area'],
                                                                         company['searchitemnbinfo'][0].get('year'))})
        # company.update({'searchitemsite': self._qianzhan_client.post_searchitemsite(company['hdencryptCode'])})

        # print "company:->", company

        return company

    def _get_search(self, url):
        # if RedisClient.get_search_url_key(url):
        #     return

        response = self._qianzhan_client.get_search(url)


        soup = BeautifulSoup(response.text, 'lxml')

        link_li_list = soup.select("body ul[class='list-search'] li p[class='tit'] a")
        for tag in link_li_list:
            href = tag['href']
            company_name = tag.text
            company_url = urljoin("http://qiye.qianzhan.com/", href)
            if RedisClient.get_company_name_detail_key(company_name):
                continue
            # if QianzhanDB.is_detail_had(company_name):
            #     continue
            # if RedisClient.get_company_url_detail_key(url):
            #     continue
            logging.info("company_name:->%s" % company_name)
            try:
                company = self._get_company(company_url)
                if company:
                    company.update({"from.chinabidding": 1})
                    QianzhanDB.upsert_company_detail(company)  # upsert company
                    RedisClient.set_company_name_detail_key(company_name)
                    # RedisClient.set_company_url_detail_key(url)
            except Error302, err:
                logging.exception("get_company Error302, company_name:->%s, e:->%s" % (company_name, err))
                raise err
            except Error403, err:
                logging.exception("get_company Error403, company_name:->%s, e:->%s" % (company_name, err))
                raise err
            except Error400, err:
                logging.exception("get_company Error400, company_name:->%s, e:->%s" % (company_name, err))
                # raise err
            except Error404, err:
                logging.exception("get_company Error404, company_name:->%s, e:->%s" % (company_name, err))
                # raise err
            except Exception, e:
                # logging.exception("get_company exception, company_name:->%s, e:->%s" % (company_name, e))
                # pass
                raise e
                # break
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

        cur = ChinabiddingDB.get_company_names()
        i = 0
        for item in cur:
            i += 1
            search_key = item['company_name']
            search_key = search_key.strip()
            logging.info("i========================: %s" % i)
            if RedisClient.get_search_key_detail_key(search_key):
                continue
            logging.info(
                "++++++crawl zhaopin:->search_key: %s" % search_key)
            url = "http://qiye.qianzhan.com/search/qy/" + urllib.quote(
                search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC"

            try:
                self._get_search(url)
                RedisClient.set_search_key_detail_key(search_key)
            except Error302, err:
                raise Error302()
            except Error403, err:
                raise Error403()
            except Error400, err:
                logging.exception("_get_search Error400, search_key:->%s, e:->%s" % (search_key, err))
                RedisClient.set_search_key_detail_key(search_key)
                # raise err
            except Error404, err:
                logging.exception("_get_search Error404, search_key:->%s, e:->%s" % (search_key, err))
                RedisClient.set_search_key_detail_key(search_key)
                # raise err
            except Exception, e:
                logging.exception("_get_search:->search_key: %s, %s" % (search_key, e.message))
                pass

    def run(self):
        logging.info("+++++++++++++run++++++++++++++++")
        try:
            is_success = self._qianzhan_client.login()
            if is_success:
                self._run()
                logging.info("++++++++++++++success finish!!!++++++++")
            else:
                raise Error302()
        except Error302, err:
            logging.error(err.message)
        except Error403, err:
            logging.error(err.message)
        except Exception, e:
            logging.exception(e.message)
            pass
