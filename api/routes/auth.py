import string

from flask import request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from api import app, db
from api.forms import LoginForm
from api.models import User


@app.route('/login', methods=['GET', 'POST'])  # login route
def login():
    if request.method == 'GET':
        form = LoginForm()  # creating a form

        # rendering login page with the given form
        return render_template('auth/login.html', form=form)

    elif request.method == 'POST':
        form = request.form  # getting the form sent back
        username = form['username'].lower()  # lowering the username

        for char in username:
            if char not in string.ascii_lowercase and char not in string.digits:
                flash("Invalid Username")
                return redirect(url_for('register'))

        # the above block means that usernames must be only letters and digits

        # checking if the user exists
        exists = User.query.filter_by(username=username).first()

        if not exists:
            flash("User doesn't exist, please register an account first")
            # redirecting the user back to the login page, due to wrong username
            return redirect(url_for('login'))

        if not check_password_hash(exists.password, form['password']):
            flash("Incorrect password")
            # redirecting the user back to the login page, due to wrong password
            return redirect(url_for('login'))

        # if none of the exit conditions are met, log the user in
        login_user(exists)

        return redirect(url_for('home'))  # send the user to the home page


@app.route('/register', methods=['GET', 'POST'])  # register page
def register():
    if request.method == 'GET':
        form = LoginForm()  # creating a login form

        # rendering the register page
        return render_template('auth/register.html', form=form)

    elif request.method == 'POST':
        form = request.form  # getting the form sent back

        for char in form['username']:
            if char.lower() not in string.ascii_lowercase and char not in string.digits:
                flash("Invalid Username")
                # username must be all letters and digits
                return redirect(url_for('register'))

        # querying the user from the database
        exists = User.query.filter_by(username=form['username']).first()

        if exists:
            flash("User already exists")
            # if the username is already in use
            return redirect(url_for('register'))

        user = User(username=form['username'].lower(),
                    password=generate_password_hash(form['password']))  # creating a new User row

        db.session.add(user)
        db.session.commit()  # adding the user to the database

        login_user(user)  # logging the user in

        return redirect(url_for('home'))  # sending them to the home page


@app.route('/logout')  # logout page
@login_required
def logout():
    logout_user()  # log the user out
    flash("Logged Out")
    return redirect(url_for('login'))  # send user back to login page
