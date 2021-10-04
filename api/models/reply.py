from datetime import datetime
from api import db


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
