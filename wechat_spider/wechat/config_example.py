# -*- coding: utf-8 -*-

import pymysql.cursors

# 新榜的用户名密码
conf_newrank = {
    'username': '',
    'password': ''
}

# 数据库连接配置
conf_db = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': '',
    'password': '',
    'charset': 'utf8mb4',
    'db': 'wechat_spider',
    'cursorclass': pymysql.cursors.DictCursor
}
