# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import random
import logging
from urlparse import urljoin
from bs4 import BeautifulSoup

from captcha import read_img_file_to_string
from web_driver import new_webdriver
from exception import Error302, Error403, Error404, ErrorStatusCode, Error400


class SiteClient(object):
    def __init__(self, userId, password):
        self._userId = userId
        self._password = password
        self._webdriver = new_webdriver()
        pass

    def do_login(self):
        login_page_url = "http://qiye.qianzhan.com/usercenter/login?ReturnUrl=http%3A%2F%2Fqiye.qianzhan.com%2F"
        self._webdriver.get(login_page_url)
        user_id_input = self._webdriver.find_element_by_id('userId')
        password_input = self._webdriver.find_element_by_id('password')
        verifycode_input = self._webdriver.find_element_by_id('verifycode')
        loginform_button = self._webdriver.find_element_by_id('loginForm_Button')
        code_img = self._webdriver.find_element_by_class_name('code-img')

        screen_shot_file = 'screen_shot.png'
        self._webdriver.save_screenshot(screen_shot_file)
        code = read_img_file_to_string(screen_shot_file, code_img.location['x'], code_img.location['y'],
                                       code_img.size['width'], code_img.size['height'])

        user_id_input.send_keys(self._userId)
        password_input.send_keys(self._password)
        verifycode_input.send_keys(code)

        loginform_button.click()
        pass

    def search(self, search_key):
        pass
