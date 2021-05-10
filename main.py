from flask import Flask, request, render_template, url_for, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fshuppprcznqku:c40eea0c5cc185e4cc9eb252ff51fb571f04b373cc612420338962638ceda414@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/d325f9dtt49eu3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'whatKey'

db = SQLAlchemy(app)
loginManager = LoginManager()
loginManager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )
    updated_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditForm(FlaskForm):
    title = StringField('Edit Title', validators=[DataRequired()])
    body = TextAreaField('Edit body', validators=[DataRequired()])
    submit = SubmitField("Submit")


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

        exists = User.query.filter_by(username=username).first()

        if not exists:
            flash("User doesn't exist, please register an account first")
            return redirect(url_for('register'))

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

        return render_template('view/index.html', posts=posts, User=User)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        form = PostForm()

        return render_template('view/create.html', form=form)

    elif request.method == 'POST':
        form = request.form

        post = Post(
            title=form['title'],
            body=form['body'],
            created_date=datetime.now(),
            author_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('home'))


@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
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
                return render_template('view/edit.html', post=post, User=user, edit=True, form=form)

            return render_template('view/edit.html', post=post, User=user)

        return render_template('view/edit.html')

    elif request.method == 'POST':
        form = request.form

        if post:
            if current_user.id == user.id:
                post.body = form['body']
                post.updated_date = datetime.now()
                db.session.commit()

        return redirect(url_for('home'))


@app.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    if current_user.id == post_id:
        post = Post.query.filter_by(id=post_id).delete()
        db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
