from model.blogs import Blog
from flask import jsonify, Blueprint

timeapi = Blueprint('timeapi', __name__)

@timeapi.route('/timeline')
def timeline():
    titles = []
    blogs = Blog.query.all()
    if (len(blogs)==0):
        return jsonify(titles)
    else:
        blogs = Blog.to_json(blogs)
        blognumber = []
        for blog in blogs:
            titles.append(blog.title)
        for i in range(0,len(blogs)):
            blognumber.append(i)
        archives = dict(zip(blognumber, titles))
        return jsonify(archives)