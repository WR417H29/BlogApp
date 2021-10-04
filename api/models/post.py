from datetime import datetime
from api import db

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
