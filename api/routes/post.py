from datetime import datetime
from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user, login_required

from api import app, db
from api.forms import PostForm, EditForm
from api.models import User, Post, Reply


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
