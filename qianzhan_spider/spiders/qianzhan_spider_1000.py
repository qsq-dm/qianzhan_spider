# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time
import urllib

import scrapy

from ..items import CompanyInfoItem

from ..utils import get_gb2312_txt, get_1000_txt


class QianzhanSpider(scrapy.Spider):
    name = "qianzhan_spider_1000"

    def start_requests(self):

        txt = get_1000_txt()
        for i in range(62, len(txt)):

            for j in range(len(txt)):
                search_key = txt[i] + txt[j]
                # search_key = u'一三'
                print "++++++1000+++++++: %s %d %d %d %s" % (
                    time.strftime('%Y-%m-%d', time.localtime(time.time())), i, j, len(txt), search_key)
                # url = "http://www.qichacha.com/search?key=" + urllib.quote(search_key.encode('utf-8')) + "&index=0"
                # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
                #     search_key.encode('utf-8')) + "?o=0&area=0&areaN=%E5%85%A8%E5%9B%BD&p=1"
                # url = "http://qiye.qianzhan.com/orgcompany/searchlistview/qy/" + urllib.quote(
                #     search_key.encode('utf-8')) + "?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC&p=1"
                url = "http://qiye.qianzhan.com/search/qy/" + urllib.quote(
                    search_key.encode('utf-8')) + "/?o=0&area=11&areaN=%E5%8C%97%E4%BA%AC"

                # print url
                request = scrapy.Request(
                    url,
                    callback=self.parse
                )
                yield request


    def parse(self, response):
        link_li_list = response.xpath('//ul[@class="list-search"]/li/p[@class="tit"]/a')
        for li_sel in link_li_list:
            href = li_sel.xpath('./@href').extract_first()
            company_name = li_sel.xpath('./text()').extract_first()

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

        yield company
