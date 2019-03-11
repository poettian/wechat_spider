# -*- coding: utf-8 -*-

from wechat_spider.utils.mail import MailServer

def send_mail():
    errors = ['未通过接口抓取到信息', '数据库插入数据失败']
    mail_server = MailServer()
    mail_server.send('poettian@163.com', '微信聚合项目异常通知', '\n'.join(errors))
