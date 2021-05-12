from flask_login import UserMixin
from datetime import datetime
# importing the db object from __init__.py to access the attributes
from api import db


class User(UserMixin, db.Model):
    """
    UserMixin is a default flask_login class to inherit from to get certain attributes on User class
    User class stores information about users
    Passwords are hashed upon entry to the database
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    """
    Post class stores information about Posts that the user can submit
    it stores the ID of the User that created it
    so this information can be used later
    """
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
    """
    Reply class stores information about Replies to posts
    which is why it stores post_id and author_id
    as these attributes are used to reference the post it is on
    and the author of the reply
    """
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
