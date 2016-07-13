# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time
import urllib

import scrapy

from ..items import CompanyInfoItem

from ..utils import get_gb2312_txt


class QianzhanSpider(scrapy.Spider):
    name = "qianzhan_spider"

    def start_requests(self):

        url = "http://qiye.qianzhan.com/"

        request = scrapy.FormRequest(
            url=url,
            callback=self.parse,
        )
        yield request

    def parse(self, response):
        link_li_list = response.xpath('//div[@id="hy_middle_connect_ul_connect"]/ul/li/a')
        for li_sel in link_li_list:
            href = li_sel.xpath('./@href').extract_first()
            title = li_sel.xpath('./text()').extract_first()

            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parse_list)
            yield request

        link_li_list_2 = response.xpath('//div[@class="dqcon"]/ul/li/a')
        for li_sel in link_li_list_2:
            href = li_sel.xpath('./@href').extract_first()
            title = li_sel.xpath('./text()').extract_first()

            url = response.urljoin(href)

            for i in range(1, 1000):  # 1-1000 pages
                str = '_%d' % i
                new_url = url.replace('_1', str)
                print new_url
                request = scrapy.Request(new_url, callback=self.parse_list)
                yield request

    def parse_list(self, response):
        a_list = response.xpath('//div[@class="dqscon"]/ul/li/a')
        for sel in a_list:
            href = sel.xpath('./@href').extract_first()
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parse_company)
            yield request

        # next_page = ""

        pass

    def parse_company(self, response):
        company = CompanyInfoItem()

        gsinfocon_div = response.xpath('//div[@class="gsinfo f_l mr_t10"]/div[@class="gsinfocon"]')
        company['company_name'] = gsinfocon_div.xpath('./ul[1]/li[2]/span/text()').extract_first()
        company['business_model'] = gsinfocon_div.xpath('./ul[2]/li[2]/text()').extract_first()
        company['business_scope'] = gsinfocon_div.xpath('./ul[3]/li[2]/text()').extract_first()

        gslx_div = response.xpath('//div[@class="gsinfo f_l mr_t10"]/div[@class="gslx"]')

        company['business_address'] = gslx_div.xpath(
            './div[@class="gs_con_left]/div[@class="gslxcon"]/ul[1]/li[2]/text()').extract_first()
        company['phone'] = gslx_div.xpath(
            './div[@class="gs_con_left]/div[@class="gslxcon"]/ul[2]/li[2]/text()').extract_first()
        company['fax'] = gslx_div.xpath(
            './div[@class="gs_con_left]/div[@class="gslxcon"]/ul[3]/li[2]/text()').extract_first()
        company['mobile'] = gslx_div.xpath(
            './div[@class="gs_con_left]/div[@class="gslxcon"]/ul[4]/li[2]/text()').extract_first()
        company['link_man'] = gslx_div.xpath(
            './div[@class="gs_con_left]/div[@class="gslxcon"]/ul[5]/li[2]/text()').extract_first()

        yield company
        pass
