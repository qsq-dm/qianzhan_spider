# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyInfoItem(scrapy.Item):
    item_category = scrapy.Field()  # 分类
    item_category_num = scrapy.Field()  # 分类编号
    item_from = scrapy.Field()  # 来源 jd, bjda..
    item_from_gb2312 = scrapy.Field()  # 是否来自gb2312
    item_update_time = scrapy.Field()  # 插入时间

    province = scrapy.Field()  # 省份
    phone = scrapy.Field()  # 电话
    mobile = scrapy.Field()  # mobile
    fax = scrapy.Field()  # 传真
    link_man = scrapy.Field()  # 联系人
    city = scrapy.Field()  # 城市
    email = scrapy.Field()  # 邮箱
    introduce = scrapy.Field()  # 介绍
    people_num = scrapy.Field()  # 规模

    company_name = scrapy.Field()  # 公司名称
    unified_social_credit_code = scrapy.Field()  # 统一社会信用代码
    registration_number = scrapy.Field()  # 注册号
    organization_registration_code = scrapy.Field()  # 组织机构代码
    business_status = scrapy.Field()  # 经营状态
    business_type = scrapy.Field()  # 公司类型, 主体类型
    business_model = scrapy.Field()  # 经营模式
    register_date = scrapy.Field()  # 成立日期, 登记日期
    legal_representative = scrapy.Field()  # 法定代表人
    registered_capital = scrapy.Field()  # 注册资本
    operating_period = scrapy.Field()  # 营业期限
    registration_authority = scrapy.Field()  # 登记机关
    date_of_issue = scrapy.Field()  # 发照日期
    business_address = scrapy.Field()  # 企业地址
    english_name = scrapy.Field()  # 公司英文名称
    business_scope = scrapy.Field()  # 经营范围

    url = scrapy.Field()  # 官网

    hdencryptCode = scrapy.Field()
    hdoc_area = scrapy.Field()

    getcommentlist = scrapy.Field()
    SearchItemCCXX = scrapy.Field()
    searchitemdftz = scrapy.Field()
    searchitemnbinfo = scrapy.Field()
    searchitemnb = scrapy.Field()
    searchitemsite = scrapy.Field()

    ejinsui = scrapy.Field()


    pass
