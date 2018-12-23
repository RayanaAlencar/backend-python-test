from alayatodo import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(255),  nullable=False)
    password    = db.Column(db.String(255),  nullable=False)
    todos       = db.relationship('Todo', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username    = username
        self.password    = password

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    description = db.Column(db.String(255),  nullable=False)

    def __init__(self, user_id, description):
        self.user_id        = user_id
        self.description    = description

    def __repr__(self):
        return '<Todo %r>' % (self.description)
