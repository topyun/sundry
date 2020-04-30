# coding:utf-8
from flask import Blueprint, render_template,current_app,request
from ..models import Posts,Category
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')

@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('main/about.html')

@main.route('/waiting', methods=['GET', 'POST'])
def waiting():
    return render_template('main/waiting.html')

@main.route('/archives', methods=['GET', 'POST'])
def archives():
    # 时间，类别，全局搜索查询
    posts = Posts.query
    category = Category.query
    posts_num = Posts.query.count()
    num = Category.query.count()

    return render_template('main/archives.html', category=category,category_num=num,posts_num=posts_num)


@main.route('/good', methods=['GET', 'POST'])
def good():
    from app.models import Posts

    page = request.args.get('page',1,type=int)
    pagination = ((Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()))).paginate(page,per_page=2,error_out=False)
    posts = pagination.items

    return render_template('main/good.html',posts=posts,pagination=pagination)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):

    post = Posts.query.get_or_404(id)
    # form = CommentForm()
    # if form.validate_on_submit():
    #     comment = Comment(body=form.body.data,
    #                         post=post,
    #                         author=current_user._get_current_object())
    #     db.session.add(comment)
    #     flash(u'留言成功')
    #     return redirect(url_for('.post', id=post.id, page=-1))
    # page = request.args.get('page', 1, type=int)
    # if page == -1:
    #     page = (post.comments.count() -1) / \
    #             current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    # pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
    #     page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
    #     error_out=False)

    return render_template('main/post.html', post=post)

@main.route('/category/<int:id>')
def category(id):

    category = Category.query.get_or_404(id)
    # posts = category.posts.order_by(Posts.timestamp.desc())
    page = request.args.get('page',1,type=int)
    pagination = category.posts.order_by(Posts.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('main/category.html',category=category,posts=posts,pagination=pagination)
#
# # ------------------------------------ #
# @main.route('/secret')
# def secret():
#     return generate_password_hash('psw')
#
# @main.route('/check/<psw>')
# def check(psw):
#     # 密码校验函数：输入加密后的的值，密码
#     if check_password_hash(
#         'pbkdf2:sha256:150000$VIDe0YJP$af0438e54cc1f33f8310787c44eec57f500eafa27c0d7fbbfc56b149aff0ce1f',
#         psw
#     ):
#         return '密码正确'
#     else:
#         return '密码错误'
# # ============================ #
#
# # ---------------------------- #
# @main.route('/generate_token/')
# def generate_token():
#     s = Serializer(current_app.config['SECRET_KEY'],expires_in=3600)
#     # 加密指定数据，以字典的形式传入
#     return s.dumps({'id':10})
#
# @main.route('/activate/<token>')
# def activate(token):
#     s = Serializer(current_app.config['SECRET_KEY'])
#     try:
#         data = s.loads(token)
#     except:
#         return 'token错误'
#     return str(data.get('id'))
# # ============================ #



