# coding:utf-8

from flask import current_app
from app.extensions import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from datetime import datetime
import hashlib
import bleach
from markdown import markdown
from app.errors import ValidationError

class Posts(db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    # 回复id
    rid = db.Column(db.Integer, index=True,default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    # 指定外键
    uid = db.Column(db.Integer,db.ForeignKey('users.id'))

    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    summury = db.Column(db.Text)
    summury_html = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.uid,
                              _external=True),
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Posts(body=body)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img']
        attrs = {
            '*': ['class'],
            'a': ['href', 'rel'],
            'img': ['src', 'alt']
        }
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

    @staticmethod
    def on_changed_summury(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote', 'em', 'i',
                        'strong', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.summury_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))



db.event.listen(Posts.body, 'set', Posts.on_changed_body)
db.event.listen(Posts.summury, 'set', Posts.on_changed_summury)



class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    posts = db.relationship('Posts',backref='category',lazy='dynamic')

    @staticmethod
    def insert_categories():
        categories = [u'web开发', u'数据挖掘', u'flask', u'python', u'爬虫', u'前端开发', u'基础知识', u'笔记', u'随记']
        for category in categories:
            postcategory=Category.query.filter_by(name=category).first()
            if postcategory is None:
                postcategory = Category(name=category)
                db.session.add(postcategory)
        db.session.commit()

    def __repr__(self):
        return '<Category %r>' % self.name