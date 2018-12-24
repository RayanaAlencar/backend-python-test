from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTS_PER_PAGE = 5

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)

import alayatodo.views
