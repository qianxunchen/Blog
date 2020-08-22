from model import db
from sqlalchemy.orm import relationship

# 评论
class Comments(db.Model):
    __tablename = 'comments'
    user = relationship('User')  # 关联User
    uname = db.Column(db.String(24), db.ForeignKey('users.name')) # 用户姓名
    bid = db.Column(db.Integer, db.ForeignKey('blog.id')) # 博客标题
    id = db.Column(db.Integer, primary_key=True)
    btitle = db.Column(db.String(50))
    body = db.Column(db.String(100))
    like = db.Column(db.Integer)
    time = db.Column(db.String(24))


    @staticmethod
    def commadd(uname, bid, btitle, body,time):
        comments = Comments()
        comments.uname = uname
        comments.bid = bid
        comments.body = body
        comments.btitle = btitle
        comments.time = time
        comments.like = 0
        db.session.add(comments)
        db.session.commit()