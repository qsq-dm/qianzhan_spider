# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time
import urllib
import json

import scrapy

from ..items import CompanyInfoItem
from ..db.mongo import NeeqItemsDB

from ..utils import get_gb2312_txt, get_1000_txt

company_name_list = []


class QianzhanSpider(scrapy.Spider):
    name = "qianzhan_spider_neeq"

    def start_requests(self):

        neeq_items = NeeqItemsDB.get_neeq_items()

        for item in neeq_items:
            print "company_name: ", item['hqzqjc']
            # url = "http://www.qichacha.com/search?key=%s&index=0" % item['hqzqjc']
            url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/%s?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC&p=1" % \
                  item['hqzqjc']
            request = scrapy.Request(
                url,
                callback=self.parse
            )
            # request.meta['item_category'] = item['xxfcbj']
            request.meta['item_category_num'] = item['xxfcbj']
            yield request

    def parse(self, response):
        link_li_list = response.xpath('//ul[@class="list-search"]/li/p[@class="tit"]/a')
        for li_sel in link_li_list:
            href = li_sel.xpath('./@href').extract_first()
            company_name = li_sel.xpath('./text()').extract_first()

            if company_name not in company_name_list:
                company_name_list.append(company_name)
                url = response.urljoin(href)
                request = scrapy.Request(url, callback=self.parse_company)
                yield request

        next_page_href = response.xpath('//a[@class="next"]/@href').extract_first()
        next_page_url = response.urljoin(next_page_href)
        request = scrapy.Request(next_page_url, self.parse)
        yield request

    def parse_company(self, response):
        company = CompanyInfoItem()

        company['company_name'] = response.xpath('//h1[@class="ct_name"]/text()').extract_first()
        company['url'] = response.xpath('//a[@class="url"]/text()').extract_first()

        company['item_update_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        ul_sel = response.xpath('//ul[@class="art-basic"]')

        company['organization_registration_code'] = ul_sel.xpath('./li[1]/span[@class="info"]/text()').extract_first()
        company['registration_number'] = ul_sel.xpath('./li[2]/span[@class="info"]/text()').extract_first()
        company['legal_representative'] = ul_sel.xpath('./li[3]/span[@class="info"]/text()').extract_first()
        company['business_status'] = ul_sel.xpath('./li[4]/span[@class="info"]/text()').extract_first()
        company['registered_capital'] = ul_sel.xpath('./li[5]/span[@class="info"]/text()').extract_first()
        company['business_type'] = ul_sel.xpath('./li[6]/span[@class="info"]/text()').extract_first()
        company['register_date'] = ul_sel.xpath('./li[7]/span[@class="info"]/text()').extract_first()
        company['operating_period'] = ul_sel.xpath('./li[8]/span[@class="info"]/text()').extract_first()
        company['business_address'] = ul_sel.xpath('./li[9]/span[@class="info"]/text()').extract_first()
        company['business_scope'] = ul_sel.xpath('./li[10]/span[@class="info"]/text()').extract_first()

        ul_sel_2 = response.xpath('//ul[@class="art-org"]')

        company['province'] = ul_sel_2.xpath('./li[2]/span[@class="info"]/text()').extract_first()
        company['registration_authority'] = ul_sel_2.xpath('./li[2]/span[@class="info"]/text()').extract_first()

        company['hdencryptCode'] = response.xpath('//input[@id="hdencryptCode"]/@value')
        company['hdoc_area'] = response.xpath('//input[@id="hdoc_area"]/@value')

        url = "http://qiye.qianzhan.com/orgcompany/searchitemdftz"
        form_data = {
            'orgName': company['company_name'],
            'page': 1,
            'pagesize': 10
        }
        request = scrapy.FormRequest(url=url, formdata=form_data, callback=self.searchitemdftz)
        request.meta['company'] = company
        yield request

    def parse_searchitemdftz(self, response):
        company = response.meta['company']
        json_text = response.body
        json_obj = json.loads(json_text)
        dataList = json_obj['dataList']

        company['searchitemdftz'] = dataList
        print dataList

        url = "http://qiye.qianzhan.com/orgcompany/searchitemnbinfo"
        form_data = {
            'orgCode': company['hdencryptCode'],
            'areaCode': company['hdoc_area']
        }
        request = scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse_searchitemnbinfo)
        request.meta['company'] = company
        yield request

    def parse_searchitemnbinfo(self, response):
        company = response.meta['company']
        json_text = response.body
        json_obj = json.loads(json_text)
        dataList = json_obj['dataList']

        company['searchitemnbinfo'] = dataList

        url = "http://qiye.qianzhan.com/orgcompany/searchitemnb"
        form_data = {
            'orgCode': company['hdencryptCode'],
            'areaCode': company['hdoc_area'],
            'year': dataList[0]['year'],
        }
        request = scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse_searchitemnbinfo)
        request.meta['company'] = company
        yield request

    def parse_searchitemnb(self, response):
        company = response.meta['company']
        json_text = response.body
        json_obj = json.loads(json_text)
        dataList = json_obj['dataList']

        company['searchitemnb'] = dataList

        yield company
