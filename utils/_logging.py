# coding=utf8

import os
import logging

os.environ['DEBUG'] = '1'

LOG_PATH = './wechat_spider.log'
LOG_FORMAT = '\t'.join([
    'log_time=%(asctime)s',
    'levelname=%(levelname)s',
    'process=%(process)d',
    '%(message)s',
    'location=%(pathname)s:%(lineno)d\n'])

level = logging.DEBUG if os.getenv('DEBUG') == '1' else logging.INFO

file_handler = logging.FileHandler(filename=LOG_PATH)
file_handler.setLevel(level)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logger = logging.getLogger('wechat_spider')
logger.setLevel(level)
logger.addHandler(file_handler)