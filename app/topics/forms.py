from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, EmailField, RadioField, IntegerField, SelectMultipleField, HiddenField
from wtforms.fields import DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length

#TOPIC_CHOICES = [ (0, 'public'), (1, 'Online Only'), (2, 'Private') ]

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

class EditTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    content = TextAreaField('Content (You can use Markdown here)') 
    published = BooleanField( 'Publish')
    submit = SubmitField('Submit')

class NewCommentForm(FlaskForm):
    author_id = HiddenField()
    topic_id = HiddenField()
    content = TextAreaField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

