# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time
import urllib
import logging

from bs4 import BeautifulSoup
from urlparse import urljoin

from mongo import QianzhanDB, ChinabiddingDB
from exception import Error302, Error403, Error400, Error404
from mredis import RedisClient
from captcha import read_img_file_to_string
from web_driver import new_webdriver


class Spider(object):
    def __init__(self, userId, password):
        # self._site_client = SiteClient(userId, password)
        self._userId = userId
        self._password = password
        self._webdriver = new_webdriver()
        pass

    def login(self):
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
        searchname_input = self._webdriver.find_element_by_id('searchname')
        searchname_input.send_keys(search_key)
        search_button = self._webdriver.find_element_by_class_name('sec-btn')
        search_button.click()

        self.next_page()

    def next_page(self):
        li_list = self._webdriver.find_elements_by_xpath('//ul[@class="list-search"]/li')
        for li in li_list:
            # 拿到列表里一项的信息
            # 找到a标签,点击a标签,
            # 跳转到浏览器新窗口, 切换窗口,拿到详细信息
            detail = self.detail()
            # 保存数据
            # 关闭新窗口, 跳转回列表窗口
            # 循环





            pass
        # 拿到下一页标签,点击下一页标签
        a_next = self._webdriver.find_element_by_class_name('next')
        a_next.click()
        self.next_page()

    def detail(self):

        pass

    def run(self):
        self.login()
        for i in range(100):
            search_key = ''
            self.search(search_key)
        pass
