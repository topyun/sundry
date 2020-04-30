# coding:utf-8
from flask import render_template

def config_errorhandler(app):
    # 配置错误页面
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('errors/403.html')

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('errors/500.html')

class ValidationError(ValueError):
    pass
