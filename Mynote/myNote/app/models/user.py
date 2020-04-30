# coding:utf-8
from flask import current_app
from app.extensions import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin,db.Model):
    # 指定表名
    __tablename__ = 'users'

    # def __init__(self):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
    # 添加头像字段，并迁移数据
    icon = db.Column(db.String(64),unique=False,default='default.jpg')

    # member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # 添加关联
    # 参数说明
    # 第一个参数，唯一一个必须参数，关联模型类名
    # backref:反向引用的字段名
    # lazy:指定加载关联数据的方式，dynamic不加载数据，但是提供关联查询
    posts = db.relationship('Posts',backref='user',lazy='dynamic')


    # 对指定字段进行处理，保护字段
    @property
    def password(self):
        raise ArithmeticError('密码不可读')
    # 设置密码，加密存储
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    # 密码校验
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    # 生成用户激活的token
    def generate_activate_token(self,expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        token = s.dumps({'id': self.id})
        return token

    # 激活账户时的token校验，校验时还不知道用户信息，需要静态方法
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('id'))
        if user is None:
            # 用户不存在
            return False
        if not user.confirmed:
            user.confirmed = True
            db.session.add(user)
        return True

    # def ping(self):
        #     self.last_seen = datetime.utcnow()
        #     db.session.add(self)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
