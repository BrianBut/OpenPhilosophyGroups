from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, EmailField, RadioField, IntegerField, SelectMultipleField
from wtforms.fields import DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length

class SelectActiveGroupForm(FlaskForm):
    selected_group = RadioField(u'Group', coerce=str)
    submit = SubmitField('Submit')
    
'''
class JoinGroupForm(FlaskForm):
    groups = SelectMultipleField('OpenGroups', choices=[] )
    submit = SubmitField('Submit')
'''