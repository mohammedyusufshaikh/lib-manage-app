from flask import Blueprint, render_template, redirect, url_for, flash
from app.books.forms import BookForm, SearchForm
import requests
import re
from app.models import Books
from app.models import db
import json

books_bp = Blueprint('books_bp', __name__)


def search(pattern, data):
    result = []
    # for record in data:
    #     temp = re.search(pattern, record['title'])
    #     if temp:
    #         result.append(record['title'])
    for book in data:
        temp_1 = re.search(pattern, book.title)
        temp_2 = re.search(pattern, book.author)
        if temp_1 or temp_2:
            result.append(book)
            print(type(book))
    return result


# def fetch_api():
#     data = requests.get("https://frappe.io/api/method/frappe-library")
#     books = data.json()['message']
#     return books


@books_bp.route("/search_results", methods=["GET", "POST"])
def result_show():
    form = SearchForm()
    if form.is_submitted():
        pattern = form.search_title.data
        books = Books.query.all()
        result = search(pattern, books)
        if result:
            flash("Books Found !")
            return render_template("found.html", result=result)
        else:
            flash("Sorry! No such book found")
            return render_template("found.html")


# @books_bp.route("/books_api", methods=["GET", "POST"])
# def books_api():
#     books = fetch_api()
#
#     return render_template("books_api.html",books=books)


@books_bp.route("/get_books", methods=["GET", "POST"])
def get_books():
    form = SearchForm()
    if form.is_submitted():
        # result = search(form.search_title.data, books)
        # print(result)
        return render_template("books.html", form=form)
    books = Books.query.all()
    return render_template("books.html", data=books, form=form)


@books_bp.route("/add_book", methods=["GET", "POST"])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        data = Books(title=form.book_title.data, author=form.book_author.data, isbn=form.isbn_code.data,
                     publisher=form.publisher.data, publication_date=form.publication_date.data,
                     pages=form.pages.data, language=form.language.data, total_qty=form.total_quantity.data)

        db.session.add(data)
        db.session.commit()
        flash("Book Added Success fully")

    return render_template("add_book.html", form=form)


@books_bp.route("/edit_book/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    form = BookForm()
    book = Books.query.get_or_404(id)
    if form.validate_on_submit():
        Books.query.filter_by(id=id).update({Books.title: form.book_title.data, Books.author: form.book_author.data,
                                             Books.publication_date: form.publication_date.data, Books.publisher:
                                                 form.publisher.data, Books.pages: form.pages.data, Books.total_qty:
                                                 form.total_quantity.data, Books.isbn: form.isbn_code.data,
                                             Books.language:
                                                 form.language.data})

        db.session.commit()
        flash("book description edited successfully !")
        return redirect(url_for('books_bp.edit_book', id=book.id))

    form.book_title.default = book.title
    form.book_author.default = book.author
    form.publication_date.default = book.publication_date
    form.publisher.default = book.publisher
    form.pages.default = book.pages
    form.total_quantity.default = book.total_qty
    form.isbn_code.default = book.isbn
    form.language.default = book.language
    form.process()
    return render_template("add_book.html", form=form, data=book)


@books_bp.route("/delete_book/<int:id>", methods=["GET", "POST"])
def delete_book(id):
    book = Books.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash("book deleted successfully !")
    return redirect(url_for('books_bp.get_books'))
