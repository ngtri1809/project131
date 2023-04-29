from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

myapp_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(myapp_obj)

login_manager = LoginManager()
login_manager.init_app(myapp_obj)
login_manager.login_view = 'login'


from app import routes, models

with myapp_obj.app_context():
    db.create_all()

if __name__ == '__main__':
    myapp_obj.run()
