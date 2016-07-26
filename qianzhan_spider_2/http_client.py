# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests
import time


class HTTPClient(object):
    def __init__(self, min_time_interval=3):
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
        return self._session.post(url, data, json, **kwargs)

    def get(self, url, **kwargs):
        self._set_last_request_time()
        return self._session.get(url, **kwargs)
