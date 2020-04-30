#-*- coding:utf-8 -*-
# import
from flask import Flask,render_template
from app.config import config
from app.extensions import *
from app.views import DEFAULT_BLUEPRINT
from app.views import config_blueprint
from app.errors import config_errorhandler


def create_app(config_name):
    app = Flask(__name__)

    # 类初始化配置
    app.config.from_object(config[config_name])
    # 调用初始化函数
    config[config_name].init_app(app)
    # 调用配置扩展
    config_extensions(app)
    # 调用配置蓝本
    config_blueprint(app)
    # 调用错误显示
    config_errorhandler(app)
    # 返回应用实例
    return app


