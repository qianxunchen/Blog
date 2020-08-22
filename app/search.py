from flask import jsonify, request, Blueprint,render_template
from model.blogs import Blog


ser = Blueprint('ser', __name__)

@ser.route('/search')
def search():
    return render_template('search.html')

@ser.route('/Search',methods=['POST'])
def Search():
    data = request.form.get('search')
    data = str('%'+data+'%')
    page = 1
    tags = Blog.query.filter(Blog.title.like(data)).paginate(page,10)
    return render_template('tag.html', tags=tags)