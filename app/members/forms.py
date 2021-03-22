from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class MemberForm(FlaskForm):
    member_name = StringField('Name', validators=[DataRequired()])
    contact_no = IntegerField('Contact', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    dob = DateField('DOB', validators=[DataRequired()])
    submit = SubmitField('Save')


class SearchForm(FlaskForm):
    search_title = StringField('Search',validators=[DataRequired()])
    submit = SubmitField('Search')