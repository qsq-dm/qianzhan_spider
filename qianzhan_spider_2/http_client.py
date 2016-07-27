# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests
import time

from config import download_delay


class HTTPClient(object):
    def __init__(self, min_time_interval=download_delay):
        self._session = requests.Session()
        self._min_time_interval = min_time_interval * 1000
        self._last_request_time = -1
        pass

    def _set_last_request_time(self):
        now = time.time()
        if now - self._last_request_time < self._min_time_interval:
            sleep = self._min_time_interval - (now - self._last_request_time)
            time.sleep(sleep / 1000.0)
            pass
        self._last_request_time = time.time()
        pass

    def post(self, url, data=None, json=None, **kwargs):
        self._set_last_request_time()
        print "post:->", url, data, json
        response = self._session.post(url, data, json, **kwargs)
        print "response:->", response.status_code
        return response

    def get(self, url, **kwargs):
        self._set_last_request_time()
        print "get:->", url
        response = self._session.get(url, **kwargs)
        print "response:->", response.status_code
        return response
