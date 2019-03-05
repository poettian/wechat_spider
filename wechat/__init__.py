# -*- coding: utf-8 -*-

import time
from datetime import datetime
import traceback
import re
import os

from wechat.newrank_api import NewRankApi
from wechat.mysql import Mysql
from utils._logging import logger

def get_all_account_articles():
    api = NewRankApi()
    db = Mysql()
    try:
        accounts = db.query('select id,account_name,account_no,newrank_uuid,fetch_time from accounts where is_disabled=%s', (0,))
        if not accounts:
            logger.warn('未查询到待抓取的公众号信息')
            return
        zero = datetime.strptime(datetime.now().strftime('%Y-%m-%d') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        for account in accounts:
            account_id = account.get('id')
            account_no = account.get('account_no')
            account_name = account.get('account_name')

            # 判断抓取时间
            last_fetch_time = account.get('fetch_time')
            if not last_fetch_time is None and last_fetch_time > zero:
                logger.debug('公众号 [' + account_name + '] 当日已抓取')
                continue

            # 取 uuid
            uuid = account.get('newrank_uuid')
            if not uuid:
                uuid = api.query(account_no)
                if not uuid:
                    logger.warn('未通过接口查询到公众号 [' + account_name + '] 的 uuid')
                    continue
                db.update('update accounts set newrank_uuid=%s where id=%s', (uuid, account_id))

            # 抓取文章数据
            articles = api.download(account_no, uuid)
            if not articles:
                logger.warn('未通过接口查询到公众号 [' + account_name + '] 的历史文章数据')
                continue

            # 文章数据入库
            try:
                for article in articles:
                    url = article.get('url')
                    re_match = re.search(r'mid=(.*)&idx=(.*)&sn=(\w*)?', url)
                    mid = re_match.group(1)
                    idx = re_match.group(2)
                    sn = re_match.group(3)
                    title = article.get('title')
                    summary = article.get('summary')
                    read_count = article.get('clicksCount')
                    like_count = article.get('likeCount')
                    public_time = article.get('publicTime')
                    sql = 'INSERT INTO articles (title,summary,url,mid,idx,sn,read_count,like_count,public_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) on DUPLICATE KEY UPDATE title=%s,summary=%s,read_count=%s,like_count=%s'

                    # 应该换成execute
                    affected_rows_num = db.execute(sql, (title,summary,url,mid,idx,sn,read_count,like_count,public_time,title,summary,read_count,like_count))

                    if affected_rows_num is False:
                        raise Exception('公众号 [' + account_name + '] 历史文章数据入库失败')
            except Exception as e:
                db.rollback()
                logger.warn(str(e))
            else:
                db.commit()

            # 更新抓取时间
            db.update('update accounts set fetch_time=%s where id=%s', (datetime.now(), account_id))

            logger.info('公众号 [' + account_name + '] 历史文章数据抓取完毕')

            # 每次抓取时间间隔设为2秒
            time.sleep(2)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(str(e) + 'exception=%s' % tb)
    finally:
        db.close()