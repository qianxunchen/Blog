from model import db


# 用户
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))#
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))#

    @staticmethod
    def useradd(name, email, password):
        user = User()
        user.name = name
        user.password = password
        user.email = email
        db.session.add(user)
        db.session.commit()