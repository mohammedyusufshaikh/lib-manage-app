from flask_wtf import FlaskForm
from datetime import datetime, timedelta
from wtforms.fields import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class TransactionForm(FlaskForm):
    member_id = SelectField('Member ID',coerce=int, validators=[DataRequired()])
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    issue_date = DateField('Issue Date', validators=[DataRequired()], default=datetime.now())
    return_date = DateField('Return Date',validators=[DataRequired()], default=datetime.now() + timedelta(days=7))
    submit = SubmitField('Issue')