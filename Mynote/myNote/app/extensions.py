# coding:utf-8


# 导入扩展库类
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_pagedown import PageDown

from flask_uploads import UploadSet,IMAGES,UploadConfiguration,patch_request_class,configure_uploads


# 创建相关扩展对象
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)
pagedown = PageDown()



def config_extensions(app):
    # 配置扩展
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)

    # # 登录扩展模块
    login_manager.init_app(app)
    # # 会话保护级别：None不使用，basic基本(默认)，strong用户信息更改立即退出
    login_manager.session_protection = 'None'
    # # 设置登陆页面端点，用户访问需要登陆的页面时，未登录将自动跳转到此处
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'need to login'
    # 上传文件初始化
    configure_uploads(app,photos)
    patch_request_class(app,size=None)



