# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests
import time

from config import download_delay, default_headers, proxies

import logging


class HTTPClient(object):
    def __init__(self, min_time_interval=download_delay):
        self._session = requests.Session()
        self._session.headers.update(default_headers)
        self._min_time_interval = min_time_interval * 1000
        self._last_request_time = -1

        self._current_proxies = {"http": proxies}
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

    def post(self, url, data=None, json=None):
        self._set_last_request_time()

        logging.info("<POST %s> %s" % (url, data))
        # try:
        response = self._session.post(url, data=data, json=json, proxies=self._current_proxies, allow_redirects=False)
        logging.info("<response %d>" % response.status_code)
        # if response.status_code not in (200, 302):
        #     # self._refresh_proxy()
        #     return self.post(url, data, json, **kwargs)
        # except Exception, e:
        # self._refresh_proxy()
        # return self.post(url, data, json, **kwargs)

        return response

    def get(self, url):
        self._set_last_request_time()

        logging.info("<GET %s>" % url)
        # try:
        response = self._session.get(url, proxies=self._current_proxies, allow_redirects=False)
        logging.info("<response %d>" % response.status_code)
        # if response.status_code not in (200, 302):
        #     self._refresh_proxy()
        #     return self.get(url, **kwargs)
        # except Exception, e:
        # self._refresh_proxy()
        # return self.get(url, **kwargs)
        return response
