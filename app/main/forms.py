from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, EmailField, RadioField
from wtforms.fields import DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length

'''
TOPIC_CHOICES = [ (0, 'public'), (1, 'Online Only'), (2, 'Private') ]

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(0, 32)])
    last_name = StringField('Last Name', validators=[Length(0, 32)])
    submit = SubmitField('Submit')
    continu = SubmitField('Continue')

# Form with discussion_venue
class NewTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About this topic')
    published = SelectField( '', choices=TOPIC_CHOICES, default=0 )
    submit = SubmitField('Submit')
'''
class InfoForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content (You can use Markdown here)') 
    submit = SubmitField('Submit')
'''
class EditTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    content = TextAreaField('Content (You can use Markdown here)') 
    published = SelectField( '', choices = TOPIC_CHOICES )
    submit = SubmitField('Submit')

# User editing a planned topic topic has date > min
class EditPlannedTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    content = TextAreaField('Content (You can use Markdown here)') 

class DeleteTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    submit = SubmitField('Delete Topic and all comments about it')
    continu = SubmitField('Continue without deleting')

class NewCommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()]) 
    submit = SubmitField('Submit')

class EditCommentForm(FlaskForm):
    content = TextAreaField('Content') 
    submit = SubmitField('Submit')
'''
class SetMeetingTimeForm(FlaskForm):
    options=['proposed', 'online', 'scheduled']
    discussion_date = DateField('Meeting Date')
    discussion_time = TimeField('Meeting Time')
    submit = SubmitField('Submit')
'''
########################## Used by Admin Only ####################################################


class EmailForm(FlaskForm):
    email = EmailField('Email')
    submit = SubmitField('Submit')
'''
