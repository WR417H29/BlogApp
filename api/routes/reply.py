from datetime import datetime
from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user, login_required

from api import app, db
from api.models import User, Reply, Post
from api.forms import ReplyForm, EditForm


# reply to a post
@app.route('/post/reply/<int:post_id>', methods=['GET', 'POST'])
@login_required
def reply(post_id):
    post = Post.query.filter_by(id=post_id).first()  # getting the post
    if request.method == 'GET':
        form = ReplyForm()  # creating a new form

        if not post:  # if the post doesnt exist
            flash("Cannot reply to post that doesn't exist")
            # sending the user back to the home screen
            return redirect(url_for('home'))

        # rendering the reply screen with a form
        return render_template('view/reply.html', post=post, form=form)

    elif request.method == 'POST':
        form = request.form  # getting the data back

        if len(form['body']) > 300:  # if the reply is too large
            flash("Please use less characters")
            return redirect(f'/post/reply/{post_id}')  # restart the process

        reply = Reply(
            reply=form['body'],
            created_date=datetime.now(),
            updated_date=datetime.now(),
            post_id=post_id,
            author_id=current_user.id
        )  # creating a reply

        db.session.add(reply)
        db.session.commit()  # entering it into the database

        # sending the user back to the home screen
        return redirect(url_for('home'))


# edit a reply
@app.route('/post/reply/edit/<int:reply_id>', methods=['GET', 'POST'])
@login_required
def edit_reply(reply_id):
    reply = Reply.query.filter_by(id=reply_id).first()  # get the reply
    if reply:  # if it exists
        if current_user.id != reply.author_id:
            flash("You do not have permission to edit this reply")
            return redirect(url_for('home'))  # send user home if not author

        # get the post the reply is on
        post = Post.query.filter_by(id=reply.post_id).first()
        # get the user of the reply
        user = User.query.filter_by(id=reply.author_id).first()

    if request.method == 'GET':
        form = EditForm(
            body=reply.reply
        )  # creating a form pre-filled with previous data

        if user:  # if the user exists
            if current_user.id == user.id:  # if they are logged in as the author
                return render_template('view/edit.html', editType="reply", reply=reply, User=user, edit=True, form=form, post=post)

            return render_template('view/edit.html', reply=reply, User=user)

        return render_template('view/edit.html')

        # this is all the same as with the similar route for posts, just for replies

    elif request.method == 'POST':
        form = request.form  # get data

        if len(form['body']) > 300:  # if too long
            flash("Please use less characters")
            return redirect(f'/post/reply/edit/{reply_id}')  # restart process

        if reply:
            if current_user.id == reply.author_id:
                reply.reply = form['body']
                reply.edited = True
                reply.updated_date = datetime.now()
                db.session.commit()  # editing and commiting the changes

        return redirect(url_for('home'))  # sending the user back home


# reply delete route
@app.route('/post/reply/delete/<int:reply_id>', methods=['GET', 'POST'])
@login_required
def delete_reply(reply_id):
    reply = Reply.query.filter_by(id=reply_id).first()  # getting reply
    if reply:  # if it exists
        if current_user.id != reply.author_id:
            flash("You do not have permission to delete this reply")
            # sending home if not logged in as author
            return redirect(url_for('home'))

        db.session.delete(reply)  # deleteing the reply
        db.session.commit()  # commiting

    return redirect(url_for('home'))  # sending home
