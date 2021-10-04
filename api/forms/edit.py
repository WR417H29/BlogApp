from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):  
    title = StringField('Edit Title', validators=[DataRequired()])
    body = TextAreaField('Edit body', validators=[DataRequired()])
    submit = SubmitField("Submit")
