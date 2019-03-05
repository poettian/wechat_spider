# -*- coding: utf-8 -*-

import requests
import os
from datetime import datetime
from random import random, choice
from hashlib import md5
import json

from .config import conf_newrank
from utils._logging import logger

class NewRankApi(object):

    __headers = {
        'origin': 'https://www.newrank.cn',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'authority': 'www.newrank.cn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'x-requested-with': 'XMLHttpRequest'
    }

    # 访问接口失败后重试次数和计数器
    __fail_trys = 1
    __fail_counter = 0

    def __init__(self):

        # 读取用户信息
        self.__data_file = os.path.join('.', 'wechat', 'data.json')
        if os.path.exists(self.__data_file):
            with open(self.__data_file, 'r') as f:
                data = f.read()
                newrank_user = json.loads(data) if data else None
        else:
            newrank_user = self._login()
        
        self._build_cookies(newrank_user)

    def download(self, account, uuid):
        '''
        下载数据接口

        account - 公众号的微信号
        '''

        # 构造请求参数
        request_uri = '/xdnphb/detail/getAccountArticle'
        headers = {
            'referer': self._get_url('/public/info/detail.html?account=' + account),
            **self.__headers
        }

        data = {
            'flag': True,
            'uuid': uuid,
        }
        self._rebuild_data(request_uri, data)

        # 发起请求
        resp = requests.post(self._get_url(request_uri), headers=headers, data=data, cookies=self.__cookies, timeout=30)
        resp_data = resp.json()

        if resp.status_code != 200 or resp_data.get('success') != True:
            raise Exception('公众号[' + account + '] download failed: ' + json.dumps(resp_data))

        if not isinstance(resp_data.get('value'), dict):
            # 如果无数据，第一次视为 cookie 失效，发起重试
            if self.__fail_counter < 1:
                self.__fail_counter += 1
                newrank_user = self._login()
                self._build_cookies(newrank_user)
                return self.download(account, uuid)
            else:
                raise Exception('公众号[ ' + account + '] download failed after retry')

        # 提取文章列表
        articles = resp_data.get('value').get('lastestArticle')
        if not isinstance(articles, list) or len(articles) == 0:
            return

        return articles

    def _build_cookies(self, newrank_user):
        '''构造请求 cookie'''

        if not newrank_user:
            raise Exception('empty newrank_user info when build cookies')

        self.__cookies = {
            'rmbuser': 'true',
            'name': newrank_user.get('phone'),
            'token': newrank_user.get('token'),
            'openid': newrank_user.get('wxopenid'),
            'tt_token': 'true',
            'useLoginAccount': 'true'
        }

    def _get_url(self, request_uri):
        return 'https://www.newrank.cn' + request_uri

    def _rebuild_data(self, request_uri, data):
        '''处理请求参数'''

        # 排序
        keys = list(data.keys())
        keys.sort()
        data['nonce'] = ''.join(choice('0123456789abcdef') for x in range(0, 9))
        keys.append('nonce')
        
        # 转换 bool 类型值为 str，并计算xyz
        l = []
        for k in keys:
            v = data.get(k)
            if isinstance(v, bool):
                v = str(v)
                v = v[0].lower() + v[1:]
                data[k] = v
            l.append(k + '=' + v)
        data['xyz'] = md5((request_uri + '?AppKey=joker&' + '&'.join(l)).encode('utf-8')).hexdigest()
    
    def _login(self):
        '''
        登录接口

        username - 登录新榜的用户名
        password - 登录新榜的密码
        '''

        # 构造请求参数
        request_uri = '/xdnphb/login/new/usernameLogin'
        headers = {
            'referer': self._get_url('/public/login/login.html?back=https%3A//www.newrank.cn/'),
            **self.__headers
        }
        flag = str(int(datetime.now().timestamp() * 1000)) + str(random())
        hash_password = md5((md5(conf_newrank['password'].encode('utf-8')).hexdigest() + 'daddy').encode('utf-8')).hexdigest()
        data = {
            'flag': flag,
            'identifyCode': '',
            'password': hash_password,
            'username': conf_newrank['username'],
        }
        self._rebuild_data(request_uri, data)

        # 发起请求
        resp = requests.post(self._get_url(request_uri), headers=headers, data=data, timeout=30)
        resp_data = resp.json()
        if resp.status_code != 200 or resp_data.get('success') != True:
            raise Exception('login failed: ' + json.dumps(resp_data))
        newrank_user = resp_data.get('value')

        # 用户信息写入 self.__data_file        
        with open(self.__data_file, 'w') as f:
            f.write(json.dumps(newrank_user))
        
        logger.info('登录并获取用户信息，写入数据文件')

        return newrank_user
    
    def query(self, account):
        '''
        获取新榜分配给公众号的 uuid，提供给 download 接口使用

        account - 公众号的微信号
        '''

        # 构造请求参数
        request_uri = '/xdnphb/data/weixinuser/searchWeixinDataByCondition'
        headers = {
            'referer': self._get_url('/public/info/search.html?value=' + account + '&isBind=false'),
            **self.__headers
        }
        data = {
            'filter': '',
            'hasDeal': False,
            'keyName': account,
            'order': 'relation',
        }
        self._rebuild_data(request_uri, data)

        # 发起请求
        resp = requests.post(self._get_url(request_uri), headers=headers, data=data, cookies=self.__cookies, timeout=30)
        resp_data = resp.json()

        if resp.status_code != 200 or resp_data.get('success') != True:
            raise Exception('公众号[' + account + '] query failed: ' + json.dumps(resp_data))

        if not isinstance(resp_data.get('value'), dict):
            # 如果无数据，第一次视为 cookie 失效，发起重试
            if self.__fail_counter < 1:
                self.__fail_counter += 1
                newrank_user = self._login()
                self._build_cookies(newrank_user)
                return self.query(account)
            else:
                raise Exception('公众号[ ' + account + '] query failed after retry')
        
        # 提取 uuid    
        uuid = None
        res_list = resp_data.get('value').get('result')
        if isinstance(res_list, list) and len(res_list) > 0:
            for item in res_list:
                if item.get('account') == account and item.get('uuid'):
                    uuid = item.get('uuid')
                    break

        return uuid
