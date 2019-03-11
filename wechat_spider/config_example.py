# -*- coding: utf-8 -*-

import pymysql.cursors

# 新榜的用户名密码
conf_newrank = {
    'username': 'nr_83739jrcm',
    'password': 'hzcs1234'
}

# 数据库连接配置
conf_db = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'it',
    'password': 'zad8CeHPVg0xjQ==',
    'charset': 'utf8mb4',
    'db': 'wechat_spider',
    'cursorclass': pymysql.cursors.DictCursor
}

# 日志是否记录debug
conf_log = {
    'debug': True        
}

# mail setting
conf_mail = {
    'host': 'smtp.qiye.163.com',
    'port': 994,
    'user': 'tianzw@wom-china.com',
    'password': 'agyCtrWJGXW7BvPA',
    'encryption': 'ssl',
    'from_addr': 'tianzw@wom-china.com',
    'from_name': '合众创思'
}
