from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTS_PER_PAGE = 5
MIGRATION_DIR = os.path.join('resources', 'migrations')

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db, directory=MIGRATION_DIR)
migrate.init_app(app, db, render_as_batch= True)
login = LoginManager(app)

import alayatodo.views
