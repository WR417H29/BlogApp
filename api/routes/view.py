from flask import request, render_template, url_for, redirect
from flask_login import current_user, login_required

from api import app, db
from api.models import User, Post, Reply


@app.route('/')
def index():
    if current_user.is_active:
        return redirect(url_for('home'))

    return render_template('view/index.html')


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.created_date).all()
        users = User.query.all()
        replies = Reply.query.order_by(Reply.created_date).all()

        return render_template('view/index.html', posts=posts, User=User, replies=replies)
