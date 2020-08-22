from model.tags import Tag
from model.blogs import Blog
from flask import Blueprint, request, render_template

tagapi = Blueprint('tagapi',__name__)

@tagapi.route('/tag')
def tag():
    global name
    name = request.args.get('name')
    print(name)
    return 'success'

@tagapi.route('/tags')
def tags():
    page = 1
    name = request.args.get('name')
    tags = Blog.query.filter_by(tag=name).paginate(page,1000)
    return render_template('tag.html',tags=tags)

@tagapi.route('/Tags')
def Tags():
    tags = Tag.query.filter().all()
    return render_template('tags.html', tags=tags)