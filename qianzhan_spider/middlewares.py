# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from scrapy.contrib.downloadermiddleware.redirect import BaseRedirectMiddleware
from scrapy.utils.python import to_native_str
from six.moves.urllib.parse import urljoin
import scrapy


class MyRedirectMiddleware(object):
    def process_response(self, request, response, spider):

        if response.status == 302:
            location = to_native_str(response.headers['location'].decode('latin1'))
            redirected_url = urljoin(request.url, location)
            request_new = scrapy.Request(redirected_url, spider.parse_redirect)
            request_new.meta['push_request'] = request
            return request_new
        else:
            return response
