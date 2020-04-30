from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,StringField,SelectField
from flask_pagedown.fields import PageDownField

from wtforms.validators import DataRequired,Length
from ..models.post import Category

class PostsForm(FlaskForm):
    # 想要设置字段的其他属性，可以通过render_kw完成

    # content = TextAreaField('',render_kw={'placeholder':'分享此刻心情...'}
    #                         ,validators=[DataRequired(),Length(1,128,message='字数超出限制')])
    # submit = SubmitField('发送')

    title = StringField(u'标题', validators=[DataRequired()])
    body = PageDownField(u'内容', validators=[DataRequired()])
    summury = PageDownField(u'摘要', validators=[DataRequired()])
    category = SelectField(u'分类',coerce=int)
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category
            in Category.query.order_by(Category.name).all()]


