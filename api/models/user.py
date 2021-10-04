from flask_login import UserMixin
from datetime import datetime
from api import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username
