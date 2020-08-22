from flask import Blueprint, render_template, jsonify

aboutapi = Blueprint('aboutapi', __name__)

@aboutapi.route('/about')
def about():
        return render_template('about.html')