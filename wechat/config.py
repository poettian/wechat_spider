# -*- coding: utf-8 -*-

import pymysql.cursors

# 新榜的用户名密码
conf_newrank = {
    'username': '18369593065',
    'password': '450972998'
}

# 数据库连接配置
conf_db = {
    'host': '127.0.0.1',
    'port': 33060,
    'user': 'homestead',
    'password': 'secret',
    'charset': 'utf8mb4',
    'db': 'wechat_spider',
    'cursorclass': pymysql.cursors.DictCursor
}