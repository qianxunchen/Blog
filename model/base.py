from flask import Flask
from model import db
import config


def create_app():
    app = Flask(__name__,   template_folder='../templates', static_folder='../static')
    app.config.from_object(config)
    register_plugin(app)
    return app

def register_plugin(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
