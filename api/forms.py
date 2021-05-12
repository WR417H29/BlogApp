from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):  # form to get a user login
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):  # form to get a post from a user
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditForm(FlaskForm):  # form to allow the user to edit a post
    title = StringField('Edit Title', validators=[DataRequired()])
    body = TextAreaField('Edit body', validators=[DataRequired()])
    submit = SubmitField("Submit")


class ReplyForm(FlaskForm):  # form to allow a user to reply to a post
    body = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField("Submit")
