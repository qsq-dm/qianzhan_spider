# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from selenium import webdriver
import requests

from captcha import read_body_to_string

driver = webdriver.PhantomJS()

driver.maximize_window()  # 窗口最大化, 这一步很重要,否则响应式网页,有部分菜单自动隐藏,访问不到

driver.get("http://qiye.qianzhan.com")  # 访问首页

a_login = driver.find_element_by_id('login')  # 找到登录按钮

a_login.click()  # 点击登录按钮, 进入到登录页

user_id_input = driver.find_element_by_id('userId')
password_input = driver.find_element_by_id('password')

userId = "18519769065"
password = "123456"

user_id_input.send_keys('18519769065')
password_input.send_keys('123456')

code_img = driver.find_element_by_class_name('code-img')
code_img_src = code_img.get_attribute('src')

# driver.get(code_img_src)

session = requests.Session()

cookie = []

for item in driver.get_cookies():
    cookie.append(item['name'] + "=" + item["value"])

c = ';'.join(cookie)

session.headers.update({"cookie": c})

response = session.get(code_img_src)

code = read_body_to_string(response.content)
