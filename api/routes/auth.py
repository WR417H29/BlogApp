import string

from flask import request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from api import app, db
from api.forms.login import LoginForm
from api.models.user import User


@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'GET':
        form = LoginForm()  
        return render_template('auth/login.html', form=form)

    elif request.method == 'POST':
        form = request.form  
        username = form['username'].lower()

        for char in username:
            if char not in string.ascii_lowercase and char not in string.digits:
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
