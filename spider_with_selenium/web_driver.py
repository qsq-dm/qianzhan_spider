# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def new_webdriver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
    )
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    # driver = webdriver.Chrome()
    # driver = webdriver.Firefox()

    # driver.implicitly_wait(5)  # seconds
    driver.maximize_window()  # 窗口最大化, 这一步很重要,否则响应式网页,有部分菜单自动隐藏,访问不到
    return driver
