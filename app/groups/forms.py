from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, EmailField, RadioField, IntegerField, SelectMultipleField, HiddenField
from wtforms.fields import DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length

class NewGroupForm(FlaskForm):
    groupname = StringField('The Name of Your New Group')
    category = SelectField('What Kind of Group')
    founder = HiddenField()
    submit = SubmitField('Submit')

'''
class DeleteGroupForm(FlaskForm):
    groupname = StringField('Group Name')
    submit = SubmitField('Submit')

class SelectActiveGroupForm(FlaskForm):
    selected_group = RadioField(u'Group', coerce=str)
    submit = SubmitField('Submit')

class JoinGroupForm(FlaskForm):
    groups = SelectMultipleField('OpenGroups', choices=[] )
    submit = SubmitField('Submit')
'''