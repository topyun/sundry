# coding:utf-8
from flask import Blueprint,render_template,flash,redirect,url_for,current_app,request,abort
from app.forms import RegisterForm,LoginForm,PasswordForm,IconForm,PostsForm
from app.email import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models import User,Posts,Category
from app.extensions import db,LoginManager,photos
from flask_login import login_user,logout_user,login_required,current_user
import random
import os
from PIL import Image


user = Blueprint('user',__name__)


@user.before_app_request
def before_request():
    if current_user.is_authenticated:
        # current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'user.' \
                and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('user/unconfirmed.html')


@user.route('/confirm')
@login_required
def resend_confirmation():  # 重新发送确认邮件

    token = current_user.generate_activate_token()
    send_email(current_user.email, '账户激活', 'email/account_activate', token=token, username=current_user.username)
    flash('a confirm email has been sent to your email.')
    return redirect(url_for('user.login'))



@user.route('/login/',methods=['GET','POST'])
def login():

    form = LoginForm()
    if current_user.is_authenticated:
        if current_user.confirmed:
            flash('您已登陆.')
            return redirect(url_for('main.index'))
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('无效用户名')
        elif u.verify_password(form.password.data):
            if not u.confirmed:
                return render_template('user/unconfirmed.html')
            else:
                # 验证通过，用户登录,并完成记住我功能
                login_user(u,remember=form.remember_me.data)
                # 如果有下一跳跳转地址就跳转到下一地址，没有进入管理页面
                return redirect(request.args.get('next') or url_for('user.profile'))
        else:
            flash('无效密码')
            # return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)

@user.route('/register/',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 有效提交

        # 创建对象，写入数据库
        u = User(username=form.username.data,password=form.password.data,email=form.email.data)
        # 发送激活邮件
        # s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        db.session.add(u)
        db.session.commit()
        # 生成校验条件
        token = u.generate_activate_token()

        flash('激活邮件已发送，请查收')
        send_email(form.email.data,'账户激活','email/account_activate',token=token,username=form.username.data)
        return redirect(url_for('user.login'))
    return render_template('user/register.html',form=form)


@user.route('/activate/<token>')
def activate(token):
    # s = Serializer(current_app.config['SECRET_KEY'])
    # try:
    #     data = s.loads(token)
    # except:
    #     return 'token错误'
    # return '%d号账户已激活' % data.get('id')
    if User.check_activate_token(token):
        flash('账户激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('账户激活失败')
        return redirect(url_for('main.index'))


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('已经退出登录')
    return redirect(url_for('main.index'))


@user.route('/manage/')
@login_required
def profile():
    return render_template('user/profile.html')


@user.route('/change_password/',methods=['GET','POST'])
@login_required
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_psw.data):
            current_user.password=form.new_psw.data
            db.session.add(current_user)
            flash('密码已修改完')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误')
            return redirect(url_for('user.change_password'))
    return render_template('user/change_password.html',form=form)

@user.route('/change_icon/',methods=['GET','POST'])
@login_required
def change_icon():
    form = IconForm()
    if form.validate_on_submit():
        # 生成随机文件名
        suffix = os.path.splitext(form.icon.data.filename)[1]
        name = rand_str() + suffix
        photos.save(form.icon.data,name=name)
        # 生成缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],name)
        img = Image.open(pathname)
        img.thumbnail((64,64))
        img.save(pathname)
        # 更换头像
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))
        # 保存新头像
        current_user.icon = name
        db.session.add(current_user)
        flash('头像已上传更新')
    return render_template('user/change_icon.html',form=form)


# 生成随机字符串
def rand_str(length=32):
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for _ in range(length))



@user.route('/getnote/',methods=['GET','POST'])
@login_required
def  note():
    form = PostsForm()
    post = Posts()
    if form.validate_on_submit():
        u = current_user._get_current_object()
        post.title = form.title.data
        post.body = form.body.data
        post.summury = form.summury.data
        post.category = Category.query.get(form.category.data)
        post.uid = u.id
        db.session.add(post)
        flash('已发送')
        return redirect(url_for('main.good'))
    return render_template('user/getnote.html',form=form)

@user.route('/editnote/<int:id>', methods=['GET', 'POST'])
@login_required
def editnote(id):
    post = Posts.query.get_or_404(id)
    # if current_user != post.author and \
    #         not current_user.can(Permission.ADMINISTER):
    #     abort(403)
    form = PostsForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.body=form.body.data
        post.summury=form.summury.data
        post.category=Category.query.get(form.category.data)
        db.session.add(post)
        flash(u'文章已更新')
        return redirect(url_for('main.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.summury.data = post.summury
    form.category.data = post.category_id
    return render_template('user/editnote.html', form=form)

@user.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):

    post = Posts.query.get_or_404(id)
    title = post.title
    db.session.delete(post)
    flash(f'文章[ { title } ]已删除')
    return redirect(url_for('main.good'))


@user.route('/batchop/', methods=['GET', 'POST'])
@login_required
def manage_del_mod():
    from app.models import Posts
    page = request.args.get('page', 1, type=int)
    pagination = ((Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()))).paginate(page, per_page=2,                                                                             error_out=False)
    posts = pagination.items
    # return render_template('main/good.html', posts=posts, pagination=pagination)

    post_ids = request.values.getlist('array')
    print(post_ids)
    #提交删除后为跳转刷新
    if post_ids:
        for post_id in post_ids:
            post = Posts.query.get_or_404(int(post_id))
            title = post.title
            db.session.delete(post)
            # todo 改为弹窗
            flash(f'文章[ { title } ]已批量删除')
        return redirect(url_for('user.manage_del_mod'))
    return render_template('user/batchop.html',posts=posts, pagination=pagination)
