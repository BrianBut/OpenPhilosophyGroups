from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, IntegerField, EmailField, BooleanField, HiddenField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, Length

ROLE_CHOICES = [ (0, 'None'), (1, 'Guest'), (2, 'User'), (3, 'Moderator'), (4, 'Administrator') ]

class RescheduleTopicForm(FlaskForm):
    discussion_datetime = StringField( 'DateTime')
    published = IntegerField('public (=0, online=1, private=2)' )
    submit = SubmitField('Submit')

class ConfirmDeleteForm(FlaskForm):
    confirmed = SubmitField('Submit')

class EditUserForm(FlaskForm):
    email = EmailField('Email')
    role = SelectField('Role', choices = ROLE_CHOICES, default=2 )                           
    confirmed = BooleanField('confirmed')
    submit = SubmitField('Submit')
    reset_password = SubmitField('Reset Password')

class DeleteUserForm(FlaskForm):
    submit = submit = SubmitField('Delete')
    continu = SubmitField('Continue without Deleting')

class NewGroupForm(FlaskForm):
    groupname = StringField( 'Group Name')
    submit = SubmitField('Submit')

class EditGroupForm(FlaskForm):
    groupname = StringField( 'Group Name')
    submit = SubmitField('Submit')

class TodoForm(FlaskForm):
    group = HiddenField( 'group')
    content = TextAreaField('content')
    submit = SubmitField('Submit')