# coding=utf8

import os
import logging
from datetime import datetime
from ..config import conf_log

os.environ['DEBUG'] = '1' if conf_log['debug'] else '0'

log_dir = './log'

if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

LOG_PATH = os.path.join(log_dir, datetime.now().strftime('%Y%m%d.log'))

LOG_FORMAT = '\t'.join([
    'log_time=%(asctime)s',
    'levelname=%(levelname)s',
    'process=%(process)d',
    '%(message)s',
    'location=%(pathname)s:%(lineno)d\n'])

level = logging.DEBUG if os.getenv('DEBUG') else logging.INFO

file_handler = logging.FileHandler(filename=LOG_PATH)
file_handler.setLevel(level)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logger = logging.getLogger('wechat_spider')
logger.setLevel(level)
logger.addHandler(file_handler)
