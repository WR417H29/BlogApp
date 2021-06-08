from datetime import datetime
from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user, login_required

from api import app, db
from api.forms import PostForm, EditForm
from api.models import User, Post, Reply


@app.route('/post/create', methods=['GET', 'POST'])  # create post route
@login_required
def create():
    if request.method == 'GET':
        form = PostForm()  # creating a form for a post

        # rendering the creation page, with the form
        return render_template('view/create.html', form=form)

    elif request.method == 'POST':
        form = request.form  # getting the data sent back

        if len(form['title']) > 30:  # if the title is too long
            flash("Title too long")
            return redirect(url_for('create'))

        if len(form['body']) > 300:  # if the body is too long
            flash("Please use less characters")
            return redirect(url_for('create'))

        post = Post(
            title=str(form['title']),
            body=str(form['body']),
            created_date=datetime.now(),
            author_id=current_user.id,
            edited=False
        )  # creating a new post

        db.session.add(post)
        db.session.commit()  # adding the post to the main page

        # sending the user back to the home page
        return redirect(url_for('home'))


# edit post route
@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()  # if the post exists
    if post:  # if the post exists
        if current_user.id != post.author_id:  # if the logged in user is NOT the author of the post
            flash("You do not have permission to edit this post")
            # sending them back to the home page
            return redirect(url_for('home'))

        user = User.query.filter_by(id=post.author_id).first()
        # getting the user

    if request.method == 'GET':
        form = EditForm(
            title=post.title,
            body=post.body
        )  # creating a form with default values

        if user:  # if the user exists
            if current_user.id == user.id:  # if the logged in user is the same user as the author
                # rendering the edit page
                return render_template('view/edit.html', editType="post", post=post, User=user, edit=True, form=form, )

                """
                the reason i am checking the user id against the logged in user
                is to prevent someone from attempting to edit someone elses post
                as these checks will prevent a non-author user from editing a post
                """

            # rendering the edit page without allowing the user to edit
            return render_template('view/edit.html', post=post, User=user)

        # if the uesr doesnt exist
        return render_template('view/edit.html')

    elif request.method == 'POST':
        form = request.form  # getting the data

        if len(form['title']) > 30:  # if the title is too long
            flash("Please use a smaller title")
            return redirect(f'/post/edit/{post_id}')  # restarting the edit

        if len(form['body']) > 300:  # if the body is too long
            flash("Please use less characters")
            return redirect(f'/post/edit/{post_id}')  # restarting the edit

        if post:  # if the post exists
            if current_user.id == user.id:  # if the logged in user is the author
                post.body = form['body']
                post.edited = True
                post.updated_date = datetime.now()
                db.session.commit()  # changing and commiting the edits

        return redirect(url_for('home'))  # redirecting back to the home page


# to delete a post
@app.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()  # getting the post
    if post:  # if the post exists
        if current_user.id != post.author_id:  # if the logged in user isnt the author
            flash("You do not have permission to delete this post")
            # sending them back to the home page
            return redirect(url_for('home'))

        replies = Reply.query.filter_by(
            post_id=post_id).all()  # every reply on the post
        for reply in replies:
            db.session.delete(reply)  # deleting the replies

        db.session.delete(post)  # deleting the post
        db.session.commit()  # commiting the changes

        """
        the reason all replies are deleted as well
        is because they must not exist in order to 
        maintain referential integrity within the
        database, as replies cannot exist without
        referencing a post, so if a post is deleted,
        all replies on it must be too.
        """

    return redirect(url_for('home'))  # sending them back to the home screen
