# coding:utf-8

from .main import main
from .user import user



DEFAULT_BLUEPRINT = (
    # 蓝本，前缀

    (main,''),
    (user,'/user'),

)

def config_blueprint(app):
    # 配置蓝本
    for blue_print,url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blue_print,url_prefix=url_prefix)
