# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from selenium import webdriver
from PIL import Image

from config import userId, password
from captcha import read_img_file_to_string

# driver = webdriver.PhantomJS()
# driver = webdriver.Chrome()
driver = webdriver.Firefox()
driver.maximize_window()  # 窗口最大化, 这一步很重要,否则响应式网页,有部分菜单自动隐藏,访问不到

driver.get("http://qiye.qianzhan.com")  # 访问首页
a_login = driver.find_element_by_id('login')  # 找到登录按钮
a_login.click()  # 点击登录按钮, 进入到登录页

while True:
    user_id_input = driver.find_element_by_id('userId')
    password_input = driver.find_element_by_id('password')
    verifycode_input = driver.find_element_by_id('verifycode')
    loginform_button = driver.find_element_by_id('loginForm_Button')
    code_img = driver.find_element_by_class_name('code-img')

    driver.save_screenshot('1.png')
    im = Image.open('1.png')

    region = im.crop((code_img.location['x'],
                      code_img.location['y'],
                      code_img.location['x'] + code_img.size['width'],
                      code_img.location['y'] + code_img.size['height']))

    region = region.resize((64, 28), Image.ANTIALIAS)
    region.save('2.png')

    code = read_img_file_to_string('2.png')

    user_id_input.send_keys(userId)
    password_input.send_keys(password)
    verifycode_input.send_keys(code)

    loginform_button.click()
