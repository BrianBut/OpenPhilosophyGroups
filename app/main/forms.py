from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, HiddenField
from wtforms.fields import DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length

'''
# Form with discussion_venue
class NewTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About this topic')
    published = SelectField( '', choices=TOPIC_CHOICES, default=0 )
    submit = SubmitField('Submit')
'''
class NewInfoForm(FlaskForm):
    content = TextAreaField('Content (You can use Markdown here)') 
    info_category = SelectField( 'new info category',coerce=int )
    submit = SubmitField('Submit')

class InfoForm(FlaskForm):
    content = TextAreaField('Content (You can use Markdown here)') 
    submit = SubmitField('Submit')

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


class InfoForm(FlaskForm):
    #title = StringField('Title')
    content = TextAreaField('Content (You can use Markdown here)') 
    submit = SubmitField('Submit')

'''
# User editing a planned topic topic has date > min
class EditPlannedTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    content = TextAreaField('Content (You can use Markdown here)') 
'''
class DeleteTopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('About This Topic')
    submit = SubmitField('Delete Topic and all comments about it')
    continu = SubmitField('Continue without deleting')

class NewCommentForm(FlaskForm):
    author_id = HiddenField()
    topic_id = HiddenField()
    content = TextAreaField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class EditCommentForm(FlaskForm):
    author_id = HiddenField()
    topic_id = HiddenField()
    content = TextAreaField('Content') 
    submit = SubmitField('Submit')


class DeleteCommentForm(FlaskForm):
    author_id = HiddenField()
    topic_id = HiddenField()
    content = TextAreaField('Content') 
    submit = SubmitField('Delete')
    

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
