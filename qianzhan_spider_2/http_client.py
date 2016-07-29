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
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })
        self._min_time_interval = min_time_interval * 1000
        self._last_request_time = -1

        self._refresh_proxy_cur()
        pass

    def _set_last_request_time(self):
        now = time.time()
        if now - self._last_request_time < self._min_time_interval:
            sleep = self._min_time_interval - (now - self._last_request_time)
            time.sleep(sleep / 1000.0)
            pass
        self._last_request_time = time.time()
        pass

    def _refresh_proxy_cur(self):
        self._proxy_cur = ProxyDB.get_items()

    def _set_proxy(self, **kwargs):
        try:
            item = self._proxy_cur.next()
        except Exception, e:
            self._refresh_proxy_cur()
            self._set_proxy(**kwargs)
            return
        proxies = {"http": "http://%s:%s" % (item['ip'], item['port'])}
        kwargs.setdefault("proxies", proxies)

    def post(self, url, data=None, json=None, **kwargs):
        self._set_last_request_time()
        self._set_proxy(**kwargs)
        logging.info("<POST %s> %s" % (url, data))
        response = self._session.post(url, data, json, **kwargs)
        logging.info("<response %d>" % response.status_code)
        if response.status_code not in (200, 302):
            return self.post(url, data, json, **kwargs)
        return response

    def get(self, url, **kwargs):
        self._set_last_request_time()
        self._set_proxy(**kwargs)
        logging.info("<GET %s>" % url)
        response = self._session.get(url, **kwargs)
        logging.info("<response %d>" % response.status_code)
        if response.status_code not in (200, 302):
            return self.get(url, **kwargs)
        return response
