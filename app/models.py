from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    total_qty = db.Column(db.Integer, nullable=False, default=0)
    issued_qty = db.Column(db.Integer, default=0)
    isbn = db.Column(db.Integer)
    publisher = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date)
    pages = db.Column(db.Integer)
    language = db.Column(db.String(50))


class Members(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.Numeric(12), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    # fee = db.Column(db.Integer, default=0)


class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    issue_date = db.Column(db.DateTime, default=datetime.now())
    return_date = db.Column(db.DateTime)
    book_status = db.Column(db.Boolean,default=False)
    fee = db.Column(db.Integer, default=0)
