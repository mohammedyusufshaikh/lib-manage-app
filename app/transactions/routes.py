from flask import Blueprint, render_template, flash, redirect, url_for
from sqlalchemy.sql import func
from app.transactions.forms import TransactionForm
from app.models import Transactions, Books, Members
from app.models import db
from datetime import date
from sqlalchemy import desc, text
import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = 'lifesciences444@gmail.com'
EMAIL_PASSWORD = 'biological'

transactions_bp = Blueprint("transactions_bp", __name__)

Charge = 10
Late_Charge = Charge + 5


def send_mail_to_defaulters(contacts):
    msg = EmailMessage()
    get_names = []
    # for mail in contacts:
    #     get_names.append(db.session.query('name').filter(Members.email == mail).first())
    # print(get_names)
    msg['Subject'] = f'Alert Regarding Fees Due !'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts
    msg.set_content(f'Hi User,\n Your payment is due. \n Please return the book as soon as possible !')

    print(msg)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


@transactions_bp.route("/notify_member", methods=["GET", "POST"])
def notify_member():
    notify_list = []
    final_list = []
    result = db.session.query('member_id').from_statement(
        text('''select member_id from transactions where return_date < NOW() and book_status=1;''')).all()

    for r in result:
        notify_list.append(Members.query.get_or_404(r[0]))

    for r in notify_list:
        final_list.append(r.email)

    send_mail_to_defaulters(final_list)
    flash("Mail Sent Successfully To Defaulters !")
    transactions = Transactions.query.all()
    books = Books.query
    members = Members.query
    return render_template("transactions.html", transactions=transactions, books=books, members=members)


@transactions_bp.route("/add_transaction/<int:id>", methods=["GET", "POST"])
def add_transaction(id):
    form = TransactionForm()
    book = Books.query.get_or_404(id)

    if form.is_submitted():
        check_member = Members.query.filter_by(id=form.member_id.data).first()

        if (book.total_qty - book.issued_qty) > 1 and check_member is not None:
            issued_qty = book.issued_qty + 1
            print(form.member_id.data)
            data = Transactions(member_id=form.member_id.data, book_id=form.book_id.data,
                                issue_date=form.issue_date.data, return_date=form.return_date.data, book_status=True)
            Books.query.filter_by(id=id).update({Books.issued_qty: issued_qty})
            db.session.add(data)
            db.session.commit()
            flash("Book issued successfully !")
            form.book_id.default = book.id
            data = Members.query.all()
            choice_list = [(member.id, str(member.id) + "---------" + member.name) for member in data]
            form.member_id.choices = choice_list
            form.member_id.default = form.member_id.data
            form.process()
            return render_template("add_transaction.html", form=form)
        else:
            flash("Sorry! book cannot be issued due to low stock  or member not found!")
            return render_template("add_transaction.html", form=form)
    form.book_id.default = book.id
    data = Members.query.all()
    choice_list = [(member.id, str(member.id) + "---------" + member.name) for member in data]
    form.member_id.choices = choice_list

    form.process()
    return render_template("add_transaction.html", form=form)


@transactions_bp.route("/view_transaction/<int:id>", methods=["GET", "POST"])
def view_transaction(id):
    transactions = Transactions.query.filter_by(member_id=id).all()
    member = Members.query.filter_by(id=id).first()
    member_detail = Members.query
    book_detail = Books.query
    return render_template("view_transaction.html", transactions=transactions, member=member, md=member_detail,
                           bd=book_detail)


@transactions_bp.route("/transactions", methods=["GET", "POST"])
def all_transactions():
    transactions = Transactions.query.all()
    books = Books.query
    members = Members.query

    return render_template("transactions.html", transactions=transactions, books=books, members=members)


@transactions_bp.route("/get_defaulters", methods=["GET", "POST"])
def get_defaulters():
    books = Books.query
    members = Members.query
    curr_dt = date.today()
    final_list = []
    # result = db.session.query('id').filter(Transactions.return_date < curr_dt, Transactions.book_status == True).all()
    result = db.session.query('id').from_statement(
        text('''select id from transactions where return_date < NOW() and book_status=1;''')).all()
    if result:
        flash("Defaulters Found !!!")
    else:
        flash("No Defaulters ! ")
    for transaction in result:
        record = Transactions.query.get_or_404(transaction.id)
        if record.book_status:
            diff = curr_dt - record.issue_date
            final_charge = (diff.days - 7) * Late_Charge + (7 * Charge)
            record.fee = final_charge
            final_list.append(record)

    return render_template("transactions.html", transactions=final_list, books=books, members=members)


@transactions_bp.route("/edit_transaction/<int:t_id>", methods=["GET", "POST"])
def edit_transaction(t_id):
    transaction = Transactions.query.get_or_404(t_id)
    form = TransactionForm()
    if form.is_submitted():
        print(form.return_date.data)
        Transactions.query.filter_by(id=transaction.id).update({Transactions.book_id: form.book_id.data,
                                                                Transactions.member_id: form.member_id.data,
                                                                Transactions.issue_date: form.issue_date.data,
                                                                Transactions.return_date: form.return_date.data})
        db.session.commit()
        flash("Transaction edited successfully !")
        return redirect(url_for('transactions_bp.view_transaction', id=transaction.member_id))
    form.book_id.default = transaction.book_id
    data = Members.query.all()
    choice_list = [(member.id, str(member.id) + "-----------" + member.name) for member in data]
    form.member_id.choices = choice_list
    form.member_id.default = transaction.member_id
    form.issue_date.default = transaction.issue_date
    form.return_date.default = transaction.return_date
    form.submit.label.text = 'Update'
    form.process()
    return render_template("edit_transaction.html", transaction=transaction, form=form)


# @transactions_bp.route("/filter", methods=["GET", "POST"])
# def filter_transaction():
#     members = Members.query.all()
#     trans_filter = db.session.query(Transactions.member_id, func.sum(Transactions.fee)).group_by(Transactions.member_id)
#     print(trans_filter.all())
#     return "OK"


@transactions_bp.route("/return_transaction/<int:book_id>/<int:member_id>", methods=["GET", "POST"])
def return_transaction(book_id, member_id):
    book = Books.query.get_or_404(book_id)
    issued_qty = book.issued_qty - 1
    Books.query.filter_by(id=book_id).update({Books.issued_qty: issued_qty})
    transaction = Transactions.query.filter_by(member_id=member_id, book_id=book_id, book_status=True).first()
    no_of_days = transaction.return_date - transaction.issue_date
    if no_of_days.days <= 7:
        final_charge = no_of_days.days * Charge
        Transactions.query.filter_by(id=transaction.id).update(
            {Transactions.book_status: False, Transactions.fee: final_charge})
        print(final_charge)
    else:
        final_charge = (no_of_days.days - 7) * Late_Charge + (7 * Charge)
        Transactions.query.filter_by(id=transaction.id).update(
            {Transactions.book_status: False, Transactions.fee: final_charge})

    db.session.commit()
    flash("book returned successfully")
    return redirect(url_for('transactions_bp.view_transaction', id=member_id))
