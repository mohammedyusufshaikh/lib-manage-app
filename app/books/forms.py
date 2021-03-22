from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class BookForm(FlaskForm):
    book_title = StringField('Book Title', validators=[DataRequired()])
    book_author = StringField('Author', validators=[DataRequired()])
    isbn_code = IntegerField('ISBN', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    publication_date = DateField('Publication Date', validators=[DataRequired()])
    pages = IntegerField('Pages')
    language = StringField('Language', validators=[DataRequired()])
    total_quantity = IntegerField('Quantity')
    submit = SubmitField('Save')


class SearchForm(FlaskForm):
    search_title = StringField('Search',validators=[DataRequired()])
    submit = SubmitField('Search')