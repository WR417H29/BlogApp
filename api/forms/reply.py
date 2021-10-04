from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ReplyForm(FlaskForm):  
    body = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField("Submit")
