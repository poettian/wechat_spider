# -*- coding: utf-8 -*-

from .wechat import get_all_account_articles
from .utils.mail import MailServer

def hzcs_articles():
    errors = get_all_account_articles()
    if len(errors) > 0:
        mail_server = MailServer()
        mail_server.send('poettian@163.com', '微信聚合项目异常通知', '<br/><br/>'.join(errors))