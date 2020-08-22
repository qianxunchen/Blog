from model.blogs import Blog
from model import db
from model.comments import Comments
from model.user import User
from model.tags import Tag
from flask import Blueprint,jsonify, request,render_template,make_response
import time
import hashlib


blogapi = Blueprint('blogapi', __name__)


global cookies
cookies = []




#获取数据进行分页
@blogapi.route('/')
def homepages():
    page = int(request.args.get('page') or 1)
    # paginate方法返回一个sqlalchemy.Pagination类型对象
    # page是查询的页码，后面的是每一页显示的数量
    blogs = Blog.query.order_by(Blog.id.desc()).paginate(page,3)
    tags = Tag.query.filter().all()
    return render_template('index.html',pagination=blogs, tags=tags)


@blogapi.route('/blog')
def blog():
    global id
    id = request.args.get('id')
    return "success"

@blogapi.route('/blogs')
def blogs():
    id = request.args.get('id')
    blogdata = Blog.query.filter_by(id=id).first()
    comments = Comments.query.filter_by(bid=id).all()
    new_read = blogdata.read + 1
    Blog.query.filter_by(id=id).update({'read': new_read})
    db.session.commit()
    if not blogdata:
        return render_template('no_find.html')
    else:
        body = open(blogdata.path,"r",encoding="utf-8")
        body = body.read()
        return render_template('blog.html',data=blogdata,body=body,comments=comments)

@blogapi.route('/login_uu')
def login_uu():
    return render_template('/login_u.html')

#登陆
@blogapi.route('/login_u',methods=['POST'])
def login_u():
    data = request.get_json()
    passwd = data['password']
    name = data['name']
    password = md(passwd)
    data = User.query.filter_by(name=name, password=passwd).first()
    if(data):
        resp = make_response(jsonify({"msg": "ok"}))
        '''
            设置cookie,默认有效期是临时cookie,浏览器关闭就失效
            可以通过 max_age 设置有效期， 单位是秒
        '''''
        cookie = password
        cookies.append(cookie)
        resp.set_cookie("uname", name)
        resp.set_cookie("cookie", cookie)#分两次设置cookie的key-value值，一起设置只能获得第一个
        return resp,cookie
    else:
        return jsonify({"msg": "账号或密码错误！"})

#注册
@blogapi.route('/logon_u')
def logon_u():
    return render_template('/logon.html')

@blogapi.route('/logon',methods=['POST'])
def logon():
    name = request.values.get('name')
    password = request.values.get('passwd')
    email = request.values.get('email')
    User.useradd(name=name,email=email,password=password)
    return render_template('login_u.html')

@blogapi.route('/comment',methods=['GET','POST'])
def comment():
    passwd = request.cookies.get('cookie')
    name = request.cookies.get('uname')
    data = request.get_json()
    comments = data['comment']
    bid = data['id']
    blog = Blog.query.filter_by(id=bid).first()
    title = blog.title
    if (passwd in cookies):
        Time = time.strftime('%Y-%m-%d')
        Comments.commadd(uname=name, bid=bid, btitle=title, body=comments, time=Time)
        return jsonify({"msg":"ok"})
    return jsonify({"msg":"ee"}),201

@blogapi.route('/comment_like')
def comment_like():
    passwd = request.cookies.get('cookie')
    if (passwd in cookies):
        id = request.args.get('id')
        data = Comments.query.filter_by(id=id).first()
        like = data.like
        Comments.query.filter_by(id=id).update({'like': like+1})
        db.session.commit()
        return jsonify({"msg": "ok"})
    return jsonify({"msg": "error"}),201

@blogapi.route('/comments_reply',methods=['POST'])
def comments_reply():
    passwd = request.cookies.get('cookie')
    name = request.cookies.get('uname')
    data = request.get_json()
    bid = data['bid']
    comment = "@"+data['comment']
    blog = Blog.query.filter_by(id=bid).first()
    title = blog.title
    if (passwd in cookies):
        Time = time.strftime('%Y-%m-%d')
        Comments.commadd(uname=name, bid=bid, btitle=title, body=comment, time=Time)
        return jsonify({"msg":"ok"})
    return jsonify({"msg": "error"}),201

def md(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    pass_md =md5.hexdigest()
    # pass_md = str(pass_md)
    return pass_md

def login_auth(cookie):
    if(cookie in cookies):
        return True
    else:
        return False