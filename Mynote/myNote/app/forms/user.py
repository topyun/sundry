# coding:utf-8

from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
# 导入字段
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField
# 导入验证器类
from wtforms.validators import DataRequired,Email,EqualTo,Length
from app.models import User
from app.extensions import photos


# 注册表单类
class RegisterForm(FlaskForm):
    username  = StringField('用户名',validators=[DataRequired(),Length(6,19,message='用户名长度在6~18个字符之间')])
    password  = StringField('密码',validators=[DataRequired(),Length(6,19,message='密码长度在6~18个字符之间')])
    confirm = PasswordField('确认密码',validators=[EqualTo('password',message='两次密码不一致')])
    email = StringField('邮箱',validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('立即注册')


    # 自定义验证器，验证用户名
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在，请再想其他用户名')

    # 自定义验证器，验证邮箱
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在，请使用其他邮箱')


# 登陆表单类
class LoginForm(FlaskForm):

    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('立即登录')

# 修改密码表单类
class PasswordForm(FlaskForm):

    old_psw = StringField('原密码', validators=[DataRequired()])
    new_psw = StringField('新密码',validators=[DataRequired(),Length(6,19,message='密码长度在6~18个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('new_psw', message='两次密码不一致')])
    submit = SubmitField('确认修改')


# 修改头像表单
class IconForm(FlaskForm):

    icon = FileField('头像',validators=[FileRequired('请选择上传的文件'),FileAllowed(photos,'只能上传图片')]  )
    submit = SubmitField('点击上传')

