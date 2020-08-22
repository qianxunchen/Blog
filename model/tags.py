from model import db

# 标签
class Tag(db.Model):
    __tablename = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(24))
    tagnumber = db.Column(db.Integer)


    @staticmethod
    def tagadd(tagname,tagnumber):
        tag = Tag()
        tag.tagname = tagname
        tag.tagnumber = tagnumber
        db.session.add(tag)
        db.session.commit()

    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v