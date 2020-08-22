from model.blogs import Blog
from model import db
from model.user import User
from model.tags import Tag
from model.comments import Comments
from flask import request,jsonify,Blueprint,render_template,make_response
import time
import hashlib

adminapi = Blueprint('adminapi',__name__)

global a_cookies
a_cookies = []

@adminapi.route('/login',methods=['POST'])
def login():
    return render_template('login.html')

@adminapi.route('/login_a',methods=['POST'])
def login_a():
    name = request.values.get('name')
    passwd = request.values.get('passwd')
    password = md(passwd)
    data = User.query.filter_by(name=name,password=passwd).first()
    if(data):
        resp = make_response(render_template('editor.html'))
        '''
            设置cookie,默认有效期是临时cookie,浏览器关闭就失效
            可以通过 max_age 设置有效期， 单位是秒
        '''''
        cookie = password
        a_cookies.append(cookie)
        resp.set_cookie("uname", name)
        resp.set_cookie("cookie", cookie)
        return resp,cookie
    else:
        return "账号或者密码错误！"


@adminapi.route('/admin',methods=['GET', 'POST'])
def admin():
    passwd = request.cookies.get('cookie')
    name = request.cookies.get('uname')
    if (passwd in a_cookies and name == "wuyi"):
        print(name)
        # 如果是post方法就返回tinymce生成html代码，否则渲染editor.html
        if request.method == 'POST':
            data = request.form['content']
            title = request.form['title']
            tag = request.form['tag']
            intro = request.form['intro']
            html = '''
        <div >
            %s
        </div>
    '''
            Blogs_html = 'templates/markdown/%s.html'% title
            f = open(Blogs_html, 'w', encoding='utf-8')
            Time = time.strftime('%Y-%m-%d')
            f.write(html % data)
            f.close()
            article = Blog(title=title, tag=tag, intro=intro, path=Blogs_html, read=1, Time=Time)
            db.session.add(article)
            db.session.commit()
            tag_n = Tag.query.filter_by(tagname=tag).first()
            if tag_n:
                tagnumber = tag_n.tagnumber + 1
                Tag.tagadd(tagname=tag,tagnumber=tagnumber)
            else:
                tagnumber = 1
                Tag.tagadd(tagname=tag, tagnumber=tagnumber)
            return render_template('pushok.html')
        return render_template('editor.html')
    return render_template('login.html')

@adminapi.route('/up', methods=['POST'])
def up():
    data = request.files['file']
    filename = time.strftime('%Y%m%d_%H%M%S')
    path = ('static/images/%s.jpg') % filename
    data.save(path)
    return {"location": path}

@adminapi.route('/blog_admin')
def blog_admin():
    data = Blog.query.filter().all()
    return render_template('blog_admin.html',data=data)

@adminapi.route('/comment_admin')
def comment_admin():
    data = Comments.query.filter().all()
    return render_template('comment_admin.html',data=data)

#删除文章
@adminapi.route('/d_blog')
def d_blog():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()
    return jsonify({"msg": "ok"})

#删除评论
@adminapi.route('/d_comment')
def d_comment():
    id = request.args.get('id')
    comment = Comments.query.filter_by(id=id).first()
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"msg": "ok"})

@adminapi.route('/comment_reply')
def comment_reply():
    name = request.cookies.get('uname')
    cookie = request.cookies.get('cookie')
    comments = request.args.get('comment')
    btitle = request.args.get('btitle')
    bid = request.args.get('bid')
    if (cookie in a_cookies):
        Time = time.strftime('%Y-%m-%d')
        comments = "@"+comments
        Comments.commadd(uname=name, bid=bid, btitle=btitle, body=comments, time=Time)
        return jsonify({"msg":"ok"})
    return jsonify({"msg": "not logining"})

def md(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    pass_md =md5.hexdigest()
    # pass_md = str(pass_md)
    return pass_md

def login_auth(cookie):
    if(cookie in a_cookies):
        return True
    else:
        return False