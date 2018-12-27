from werkzeug.security import generate_password_hash,check_password_hash
from alayatodo import db,ma
from sqlalchemy.orm import validates
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username    = db.Column(db.String(255), nullable=False)
    password    = db.Column(db.String(255), nullable=False)
    todos       = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    user_id     = db.Column(db.Integer,db.ForeignKey('users.id'),
                            nullable=False)
    description = db.Column(db.String(255),nullable=False)
    complete    = db.Column(db.Boolean,default=0,nullable=False)

    @validates('description')
    def validate_description(self,key,description):
        if not description:
            raise AssertionError('No description provided')
        return description

    def __init__(self,user_id,description,complete):
        self.user_id        = user_id
        self.description    = description
        self.complete       = complete

    def __repr__(self):
        return '<Todo %r>' % (self.description)

class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id','user_id','description','complete')
