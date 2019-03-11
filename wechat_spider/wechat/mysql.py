# -*- coding: utf-8 -*-

import os
import pymysql.cursors

from ..config import conf_db

class Mysql(object):

    # 数据表默认字段
    __tables = {
        'accounts': {
            'account_name': '',
            'account_no': '',
            'head_image': '',
            'newrank_uuid': '',
            'fetch_time': None,
            'public_time': None,
            'is_disabled': 0
        },
        'articles': {
            'account_id': 0,
            'title': '',
            'summary': '',
            'url': '',
            'mid': '',
            'idx': '',
            'sn': '',
            'read_count': 0,
            'like_count': 0,
            'public_time': '1970-01-01 00:00:01'
        }
    }

    def __init__(self):
        self.__connection = pymysql.connect(host=conf_db['host'],
                                            user=conf_db['user'],
                                            password=conf_db['password'],
                                            port=conf_db['port'],
                                            db=conf_db['db'],
                                            charset=conf_db['charset'],
                                            cursorclass=conf_db['cursorclass'])

    def batch_insert(self, table, data):
        '''批量插入数据'''
        
        table_defaults = self.__tables.get(table)
        if not table_defaults or not isinstance(data, list):
            return False
        keys = table_defaults.keys()
        binging_values = []
        for row in data:
            if not isinstance(row, dict):
                continue
            row = {**table_defaults, **row}
            binging_values.append(tuple(row.values())) 
        sql = 'INSERT INTO ' + table + ' (' + ','.join(keys) + ') VALUES (' + ','.join(['%s' for x in range(0, len(keys))]) + ')'

        try:
            with self.__connection.cursor() as cursor:
                affected_rows_num = cursor.executemany(sql, binging_values)

            self.__connection.commit()

            return affected_rows_num
        except:
            return False

    # 有待进一步完善
    def query(self, sql, binging_values=None):
        '''查询数据'''

        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(sql, binging_values)
                results = cursor.fetchall()

            return results
        except:
            return None

    # 有待进一步完善
    def update(self, sql, binging_values):
        '''更新数据'''

        try:
            with self.__connection.cursor() as cursor:
                affected_rows_num = cursor.execute(sql, binging_values)

            self.__connection.commit()

            return affected_rows_num
        except:
            return False

    def execute(self, sql, binging_values):
        with self.__connection.cursor() as cursor:
            affected_rows_num = cursor.execute(sql, binging_values)
        return affected_rows_num

    def commit(self):
        self.__connection.commit()

    def rollback(self):
        self.__connection.rollback()

    def close(self):
        '''关闭连接'''

        self.__connection.close()