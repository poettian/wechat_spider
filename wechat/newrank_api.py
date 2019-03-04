# -*- coding: utf-8 -*-

import requests
import os
from datetime import datetime
from random import random, choice
from hashlib import md5
import json

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

    def __init__(self):
        self.__data = None
        self.__data_file = os.path.join('.', 'wechat', 'data.json')
        if os.path.exists(self.__data_file):
            with open(self.__data_file, 'r') as f:
                data = f.read()
                self.__data = json.loads(data) if data else None

    def generate_nonce(self):
        return ''.join(choice('0123456789abcdef') for x in range(0, 9))

    def get_url(self, request_uri):
        return 'https://www.newrank.cn' + request_uri

    def generate_xyz(self, request_uri, sorted_data):
        l = []
        for k, v in sorted_data.items():
            if v is True:
                v = 'true'
            l.append(k + '=' + v)
        return md5((request_uri + '?AppKey=joker&' + '&'.join(l)).encode('utf-8')).hexdigest()
    
    def login(self, username, password):
        '''登录接口'''

        # 构造请求参数
        request_uri = '/xdnphb/login/new/usernameLogin'
        headers = {
            'referer': 'https://www.newrank.cn/public/login/login.html?back=https%3A//www.newrank.cn/',
            **self.__headers
        }
        flag = str(int(datetime.now().timestamp() * 1000)) + str(random())
        hash_password = md5((md5(password.encode('utf-8')).hexdigest() + 'daddy').encode('utf-8')).hexdigest()
        nonce = self.generate_nonce()
        data = {
            'flag': flag, 
            'identifyCode': '', 
            'password': hash_password, 
            'username': username, 
            'nonce': nonce
        }
        data['xyz'] = self.generate_xyz(request_uri, data)

        # 发起请求
        resp = requests.post(self.get_url(request_uri), headers=headers, data=data, timeout=10)
        resp_data = resp.json()
        if resp.status_code != 200 or resp_data.get('success') != True:
            raise Exception('login fail:' + json.dumps(resp_data))

        # 写 cookie file        
        with open(self.__data_file, 'w') as f:
            f.write(json.dumps(resp_data.get('value')))

        # todo 记录日志

    def query(self, account):
        '''请求数据接口'''

        if self.__data is None:
            raise Exception('user data is None')

        # 构造请求参数
        request_uri = '/xdnphb/detail/getAccountArticle'
        headers = {
            'referer': self.get_url('/public/info/detail.html?account=' + account),
            **self.__headers
        }
        flag = True
        nonce = self.generate_nonce()
        data = {
            'flag': flag,
            'uuid': '6F8CA1A8DC0AE24D000B02FCAD0AD90A', # 这里的uuid
            'nonce': nonce
        }
        data['xyz'] = self.generate_xyz(request_uri, data)
        # 这里有点疑问，True 为什么就不行呢
        cookies = {
            'rmbuser': 'true',
            'name': self.__data.get('phone'),
            'token': self.__data.get('token'),
            'openid': self.__data.get('wxopenid'),
            'tt_token': 'true',
            'useLoginAccount': 'true'
        }

        # 发起请求
        resp = requests.post(self.get_url(request_uri), headers=headers, data=data, cookies=cookies, timeout=10)
        resp_data = resp.json()
        print(resp_data)
        os._exit(0)
        if resp.status_code != 200 or resp_data.get('success') != True:
            raise Exception(account + ' query fail:' + json.dumps(resp_data))

        print(resp.get('value'))