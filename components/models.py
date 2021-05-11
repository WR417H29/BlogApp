from flask_login import UserMixin
from datetime import datetime
from components import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    edited = db.Column(db.Boolean, nullable=False, default=False)
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )
    updated_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reply = db.Column(db.Text, nullable=False)
    edited = db.Column(db.Boolean, nullable=False, default=False)
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )
    updated_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Reply %r>' % self.reply
