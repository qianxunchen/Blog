from model import db

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))#标题
    tag = db.Column(db.String(50))  #标签
    read= db.Column(db.Integer)  #阅读量
    intro = db.Column(db.String(100)) # 简介
    path = db.Column(db.String(100))#markdown文本路径
    Time = db.Column(db.String(50))#

    @staticmethod
    def blogadd(title, tag, read, intro, path, Time):
        blog = Blog()
        blog.title = title
        blog.tag = tag
        blog.read = read
        blog.intro = intro
        blog.path = path
        blog.Time = Time
        db.session.add(blog)
        db.session.commit()

    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v