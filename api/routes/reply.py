from datetime import datetime
from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user, login_required

from api import app, db
from api.models import User, Reply, Post
from api.forms import ReplyForm, EditForm


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
