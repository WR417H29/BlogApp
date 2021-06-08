from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user, login_required

from api import app, db
from api.models import User, Post, Reply


@app.route('/')  # index route
def index():
    if current_user.is_active:  # if logged in
        return redirect(url_for('home'))  # sending user to home screen

    # rendering index if not logged in
    return render_template('view/index.html')


@app.route('/home', methods=['GET', 'POST'])  # home route
@login_required
def home():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.created_date).all()
        users = User.query.all()
        replies = Reply.query.order_by(
            Reply.created_date).all()  # getting all data

        # rendering index with posts etc.
        return render_template('view/index.html', posts=posts, User=User, replies=replies)


# profile page for users
@app.route('/profile/<string:_username>', methods=['GET', 'POST'])
def profile_view(_username):
    if request.method == 'GET':
        user = User.query.filter_by(username=_username).first()  # get user
        if not user:  # if they dont exists
            flash("User doesn't exist, please try again")
            return redirect(url_for('home'))  # send home

        posts = Post.query.filter_by(
            author_id=user.id).all()  # all the users posts
        # send to page with user posts
        return render_template('view/profile.html', posts=posts, user=user, User=User)
