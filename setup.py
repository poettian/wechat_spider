#!/usr/bin/env python
# coding: utf-8

import os
from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name = 'wechat_spider',
    version = '0.1.0',
    author = 'tianzhiwei',
    author_email = 'poettian@gmail.com',
    url = 'http://gitlab.unitechance.com/engineers/wechat_spider',
    description = '通过新榜接口抓取公众号文章信息',
    long_description = read('README.md'),
    long_description_content_type = 'text/markdown',
    license = 'MIT',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords = 'wechat articles newrank',
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires = [
        'requests'
    ],
    entry_points = {
        'console_scripts': [
            'hzcs_get_articles = wechat:get_all_account_articles',
        ]
    }
)
