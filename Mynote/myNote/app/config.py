# coding:utf-8
import os


base_dir = os.path.abspath(os.path.dirname(__name__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'biubiubiu'
    # 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件
    SB_MAIL_SUBJECT_PREFIX = '[SmallBluer]'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com' # 'smtp.biubiubiu@yunmail'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '18322597286@163.com' #'biubiubiu@yunmail'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'pyf666'

    # 使用本地依赖包
    # BOOTSTRAP_SERVER_LOCAL = True
    # TEMPLATES_AUTO_RELOAD = True

    # 文件上传 头像上传
    MAX_CONTENT_LENGTH = 16*1024*1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/uploads/photos')

    FLASK_POSTS_PER_PAGE = 2

    # 初始化
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(base_dir, 'data_dev.sqlite')

# 测试环境
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(base_dir, 'data-test.sqlite')

# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(base_dir, 'data-prod.sqlite')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}