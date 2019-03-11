# coding=utf8

from ..config import conf_mail
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, parseaddr, formataddr
from email.header import Header
import smtplib

class MailServer(object):
    """Represents an SMTP server, able to send outgoing emails, with SSL and TLS capabilities."""

    def __init__(self, timeout=60):
        self._smtp_host = conf_mail['host']
        self._smtp_port = conf_mail['port']
        self._smtp_user = conf_mail['user']
        self._smtp_pass = conf_mail['password']
        self._smtp_encryption = conf_mail['encryption']
        self._smtp_from_addr = conf_mail['from_addr']
        self._smtp_from_name = conf_mail['from_name']
        self._smtp_timeout = timeout

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def _connect(self):
        """Returns a new SMTP connection to the given SMTP server."""

        smtp_server = self._smtp_host
        smtp_port = self._smtp_port
        smtp_user = self._smtp_user
        smtp_password = self._smtp_pass
        smtp_encryption = self._smtp_encryption

        if smtp_encryption == 'ssl':
            connection = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=self._smtp_timeout)
        else:
            connection = smtplib.SMTP(smtp_server, smtp_port, timeout=self._smtp_timeout)
        if smtp_encryption == 'starttls':
            connection.starttls()

        connection.login(smtp_user, smtp_password)
        return connection

    def _build_email(self, email_to, subject, body, attachments=None, subtype='plain'):
        """Constructs an RFC2822 email.message.Message object based on the keyword arguments passed, and returns it.

           :param list email_to: list of recipient addresses (to be joined with commas)
           :param string subject: email subject (no pre-encoding/quoting necessary)
           :param string body: email body, of the type ``subtype`` (by default, plaintext).
                               If html subtype is used, the message will be automatically converted
                               to plaintext and wrapped in multipart/alternative, unless an explicit
                               ``body_alternative`` version is passed.
           :param string subtype: optional mime subtype for the text body (usually 'plain' or 'html'),
                                  must match the format of the ``body`` parameter. Default is 'plain',
                                  making the content part of the mail "text/plain".
           :param list attachments: list of (filename, filecontents) pairs, where filecontents is a string
                                    containing the bytes of the attachment

           :return: the new RFC2822 email message
        """

        msg = MIMEMultipart()
        msg['From'] = self._format_addr('%s <%s>' % (self._smtp_from_name, self._smtp_from_addr))
        msg['Subject'] = Header(subject, 'utf-8').encode() 
        msg['To'] = email_to
        msg['Date'] = formatdate()

        email_text_part = MIMEText(body or u'', _subtype=subtype, _charset='utf-8')
        msg.attach(email_text_part)

        if attachments:
            for (fname, fcontent) in attachments:
                part = MIMEBase('application', "octet-stream")
                part.set_param('name', fname)
                part.add_header('Content-Disposition', 'attachment', filename=fname)
                part.set_payload(fcontent)
                encoders.encode_base64(part)
                msg.attach(part)
        return msg

    def _send_email(self, message):
        """Sends an email"""

        try:
            smtp = self._connect()
            try:
                smtp.sendmail(self._smtp_from_addr, message['To'], message.as_string())
            finally:
                smtp.quit()
        except Exception as e:
            raise Exception("邮件发送失败:%s" % e)

    def send(self, to, subject, content, attachments=None, subtype='plain'):
        '''
        发送邮件
        to: '收件人地址',
        subject: '邮件主题',
        content: '邮件内容',
        attachments: (附件名，附件内容字节流),
        subtype: 'MIME格式'
        '''
        
        msg = self._build_email(to, subject, content, attachments, subtype)

        self._send_email(msg)
