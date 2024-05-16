from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, EmailField, RadioField, IntegerField, SelectMultipleField, HiddenField
from wtforms.fields import DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length

class NewTopicForm(FlaskForm):
    group = HiddenField()
    author_id = HiddenField()
    title = StringField('Topic Name (Title)')
    summary = TextAreaField('Summary of What the Topic is About')
    submit = SubmitField('Submit')

class EditTopicForm(FlaskForm):
    summary = TextAreaField('Summary of What the Topic is About')
    content = TextAreaField('Introductory Section')
    submit = SubmitField('Submit')