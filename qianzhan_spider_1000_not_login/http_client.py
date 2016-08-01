# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests
import time

from config import download_delay

import logging
import json

from mongo import ProxyDB


class HTTPClient(object):
    def __init__(self, min_time_interval=download_delay):
        self._session = requests.Session()
        self._session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            # Cache-Control:no-cache
            'Connection': 'keep-alive',
            # 'Cookie': 'qznewsite.uid=rssbv51ml0mwomw4k4mkycz2; qz.newsite=41A3A9C8ADE5F5073B86647E6C185D2272112F0E96AD14B275E442ED8A2B85688F50512A00FAD14DB2D485EF57054E35ECB028B44D155EE32D029A4352C6617B74BE83EB551C4D66024D7F4913B053785964ED37F3061D43BA0E8663791A1E143AC458E738C7484453887CEAB6EDEC359632DDDEAF6D585D0BD31087077296B6D97CF68F',
            'Host': 'qiye.qianzhan.com',
            # Pragma:no-cache
            'Referer': 'http://qiye.qianzhan.com/',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        })
        self._min_time_interval = min_time_interval * 1000
        self._last_request_time = -1

        # self._current_proxies = None
        # self._refresh_proxy_cur()
        # self._refresh_proxy()
        pass

    def _set_last_request_time(self):
        now = time.time()
        if now - self._last_request_time < self._min_time_interval:
            sleep = self._min_time_interval - (now - self._last_request_time)
            time.sleep(sleep / 1000.0)
            pass
        self._last_request_time = time.time()
        pass

    # def _refresh_proxy_cur(self):
    #     self._proxy_cur = ProxyDB.get_items()
    #
    # def _refresh_proxy(self):
    #     try:
    #         item = self._proxy_cur.next()
    #         # item = self._proxy_cur[1]
    #         self._current_proxies = {"http": "http://%s:%s" % (item['ip'], item['port'])}
    #         logging.info("proxy: %s" % self._current_proxies)
    #     except Exception, e:
    #         self._refresh_proxy_cur()
    #         self._refresh_proxy()

    def post(self, url, data=None, json=None, **kwargs):
        self._set_last_request_time()
        # kwargs.update({"proxies", self._current_proxies})
        # kwargs.update({"timeout", 2})
        logging.info("<POST %s> %s %s" % (url, data, kwargs))
        # try:
        response = self._session.post(url, data, json, **kwargs)
        logging.info("<response %d>" % response.status_code)
        # if response.status_code not in (200, 302):
        #     # self._refresh_proxy()
        #     return self.post(url, data, json, **kwargs)
        # except Exception, e:
        # self._refresh_proxy()
        # return self.post(url, data, json, **kwargs)

        return response

    def get(self, url, **kwargs):
        self._set_last_request_time()
        # logging.info("kwargs: %s, proxies: %s" % (kwargs, self._current_proxies))

        # kwargs.update({"proxies", self._current_proxies})
        # kwargs.update({"timeout", 2})
        logging.info("<GET %s %s>" % (url, kwargs))
        # try:
        response = self._session.get(url, **kwargs)
        logging.info("<response %d>" % response.status_code)
        # if response.status_code not in (200, 302):
        #     self._refresh_proxy()
        #     return self.get(url, **kwargs)
        # except Exception, e:
        # self._refresh_proxy()
        # return self.get(url, **kwargs)
        return response
