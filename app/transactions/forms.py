from flask_wtf import FlaskForm
from datetime import datetime
from wtforms.fields import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class TransactionForm(FlaskForm):
    member_id = IntegerField('Member ID', validators=[DataRequired()])
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    issue_date = DateField('Issue Date', validators=[DataRequired()], default=datetime.now())
    return_date = DateField('Return Date')
    submit = SubmitField('Issue')