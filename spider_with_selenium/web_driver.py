# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from selenium import webdriver


def new_webdriver():
    # driver = webdriver.PhantomJS()
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    driver.maximize_window()  # 窗口最大化, 这一步很重要,否则响应式网页,有部分菜单自动隐藏,访问不到
    return driver
