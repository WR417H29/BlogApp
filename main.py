from flask import Flask, request, render_template, url_for, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import string

from components import app, db, loginManager
from components.forms import LoginForm, PostForm, EditForm, ReplyForm
from components.models import User, Post, Reply


@loginManager.user_loader
def userLoader(userID):
    return User.query.get(int(userID))


@app.route('/')
def index():
    if current_user.is_active:
        return redirect(url_for('home'))

    return render_template('view/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()

        return render_template('auth/login.html', form=form)

    elif request.method == 'POST':
        form = request.form
        username = form['username'].lower()

        for char in form['username']:
            if char.lower() not in string.ascii_lowercase and char not in string.digits:
                flash("Invalid Username")
                return redirect(url_for('register'))

        exists = User.query.filter_by(username=username).first()

        if not exists:
            flash("User doesn't exist, please register an account first")
            return redirect(url_for('login'))

        if not check_password_hash(exists.password, form['password']):
            flash("Incorrect password")
            return redirect(url_for('login'))

        login_user(exists)

        return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = LoginForm()

        return render_template('auth/register.html', form=form)

    elif request.method == 'POST':
        form = request.form

        for char in form['username']:
            if char.lower() not in string.ascii_lowercase and char not in string.digits:
                flash("Invalid Username")
                return redirect(url_for('register'))

        exists = User.query.filter_by(username=form['username']).first()

        if exists:
            flash("User already exists")
            return redirect(url_for('register'))

        user = User(username=form['username'].lower(),
                    password=generate_password_hash(form['password']))

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged Out")
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        posts = Post.query.all()
        users = User.query.all()
        replies = Reply.query.all()

        return render_template('view/index.html', posts=posts, User=User, replies=replies)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        form = PostForm()

        return render_template('view/create.html', form=form)

    elif request.method == 'POST':
        form = request.form

        if len(form['title']) > 30:
            flash("Title too long")
            return redirect(url_for('create'))

        if len(form['body']) > 300:
            flash("Please use less characters")
            return redirect(url_for('create'))

        post = Post(
            title=form['title'],
            body=form['body'],
            created_date=datetime.now(),
            author_id=current_user.id,
            edited=False
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('home'))


@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        if current_user.id != post.author_id:
            flash("You do not have permission to edit this post")
            return redirect(url_for('home'))

        user = User.query.filter_by(id=post.author_id).first()

    if request.method == 'GET':
        form = EditForm(
            title=post.title,
            body=post.body
        )
        if user:
            if current_user.id == user.id:
                return render_template('view/edit.html', editType="post", post=post, User=user, edit=True, form=form, )

            return render_template('view/edit.html', post=post, User=user)

        return render_template('view/edit.html')

    elif request.method == 'POST':
        form = request.form

        if len(form['title']) > 30:
            flash("Please use a smaller title")
            return redirect(f'/post/edit/{post_id}')

        if len(form['body']) > 300:
            flash("Please use less characters")
            return redirect(f'/post/edit/{post_id}')

        if post:
            if current_user.id == user.id:
                post.body = form['body']
                post.edited = True
                post.updated_date = datetime.now()
                db.session.commit()

        return redirect(url_for('home'))


@app.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        if current_user.id != post.author_id:
            flash("You do not have permission to delete this post")
            return redirect(url_for('home'))

        replies = Reply.query.filter_by(post_id=post_id).all()
        for reply in replies:
            db.session.delete(reply)


        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('home'))


@app.route('/post/reply/<int:post_id>', methods=['GET', 'POST'])
@login_required
def reply(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'GET':
        form = ReplyForm()

        if not post:
            flash("Cannot reply to post that doesn't exist")
            return redirect(url_for('home'))

        return render_template('view/reply.html', post=post, form=form)

    elif request.method == 'POST':
        form = request.form

        if len(form['body']) > 300:
            flash("Please use less characters")
            return redirect(f'/post/reply/{post_id}')

        reply = Reply(
            reply=form['body'],
            created_date=datetime.now(),
            updated_date=datetime.now(),
            post_id=post_id,
            author_id=current_user.id
        )

        db.session.add(reply)
        db.session.commit()

        return redirect(url_for('home'))


@app.route('/post/reply/edit/<int:reply_id>', methods=['GET', 'POST'])
@login_required
def edit_reply(reply_id):
    reply = Reply.query.filter_by(id=reply_id).first()
    if reply:
        if current_user.id != reply.author_id:
            flash("You do not have permission to edit this reply")
            return redirect(url_for('home'))

        post = Post.query.filter_by(id=reply.post_id).first()
        user = User.query.filter_by(id=reply.author_id).first()

    if request.method == 'GET':
        form = EditForm(
            body=reply.reply
        )
        if user:
            if current_user.id == user.id:
                return render_template('view/edit.html', editType="reply", reply=reply, User=user, edit=True, form=form, post=post)

            return render_template('view/edit.html', reply=reply, User=user)

        return render_template('view/edit.html')

    elif request.method == 'POST':
        form = request.form

        if len(form['body']) > 300:
            flash("Please use less characters")
            return redirect(f'/post/reply/edit/{reply_id}')

        if reply:
            if current_user.id == reply.author_id:
                reply.reply = form['body']
                reply.edited = True
                reply.updated_date = datetime.now()
                db.session.commit()

        return redirect(url_for('home'))


@app.route('/post/reply/delete/<int:reply_id>', methods=['GET', 'POST'])
@login_required
def delete_reply(reply_id):
    reply = Reply.query.filter_by(id=reply_id).first()
    if reply:

        if current_user.id != reply.author_id:
            flash("You do not have permission to delete this reply")
            return redirect(url_for('home'))

        db.session.delete(reply)
        db.session.commit()
    
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(port=5000)
