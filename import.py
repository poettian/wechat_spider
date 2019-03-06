# -*- coding: utf-8 -*-

import os
import xlrd
import traceback
import time

from wechat.mysql import Mysql

if __name__ == '__main__':
    xlsfile = r'./wechat.xlsx'
    book = xlrd.open_workbook(xlsfile)
    sheets = book.sheet_names()
    db = Mysql()
    try:
        for name in sheets:
            sheet = book.sheet_by_name(name)
            nrows = sheet.nrows
            for i in range(nrows):
                row = sheet.row_values(i)
                data = {'account_name': row[0], 'account_no': row[1]}
                affected_rows_num = db.batch_insert('accounts', [data])
                if affected_rows_num is False:
                    print('公众号 [' + row[0] + '] 入库失败')
                    continue
                print('公众号 [' + row[0] + '] 入库完毕')
    except Exception as e:
        tb = traceback.format_exc()
        print(str(e) + 'exception=%s' % tb)
    finally:
        db.close()
