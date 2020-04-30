#-*- coding:utf-8 -*-

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app.extensions import mail

def send_async_email(app, msg):
    # 发送邮件所需上下文
    # 在新的线程中有无上下文，手动创建
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    # 从current_app代理对象中获取程序的原始实例
    app = current_app._get_current_object()
    msg = Message(app.config['SB_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                    sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # 创建线程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
