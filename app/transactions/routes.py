from flask import Blueprint, render_template, flash, redirect, url_for
from sqlalchemy.sql import func
from app.transactions.forms import TransactionForm
from app.models import Transactions, Books, Members
from app.models import db

transactions_bp = Blueprint("transactions_bp", __name__)

Charge = 5
Late_Charge = Charge + 2


@transactions_bp.route("/add_transaction/<int:id>", methods=["GET", "POST"])
def add_transaction(id):
    form = TransactionForm()
    book = Books.query.get_or_404(id)

    if form.is_submitted():
        if (book.total_qty - book.issued_qty) > 1:
            issued_qty = book.issued_qty + 1
            print(form.member_id.data)
            data = Transactions(member_id=form.member_id.data, book_id=form.book_id.data,
                                issue_date=form.issue_date.data, return_date=form.return_date.data, book_status=True)
            Books.query.filter_by(id=id).update({Books.issued_qty: issued_qty})
            db.session.add(data)
            db.session.commit()
            flash("Book issued successfully !")
        else:
            flash("Sorry! book cannot be issued due to low stock !")
    form.book_id.default = book.id
    form.process()
    return render_template("add_transaction.html", form=form)


@transactions_bp.route("/view_transaction/<int:id>", methods=["GET", "POST"])
def view_transaction(id):
    transactions = Transactions.query.filter_by(member_id=id).all()
    return render_template("view_transaction.html", transactions=transactions)


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
    form.member_id.default = transaction.member_id
    form.issue_date.default = transaction.issue_date
    form.return_date.default = transaction.return_date
    form.submit.label.text = 'Update'
    form.process()
    return render_template("edit_transaction.html", transaction=transaction, form=form)


@transactions_bp.route("/filter", methods=["GET", "POST"])
def filter_transaction():
    members = Members.query.all()
    trans_filter = db.session.query(Transactions.member_id, func.sum(Transactions.fee)).group_by(Transactions.member_id)
    print(trans_filter.all())
    return "OK"


@transactions_bp.route("/return_transaction/<int:book_id>/<int:member_id>", methods=["GET", "POST"])
def return_transaction(book_id, member_id):
    book = Books.query.get_or_404(book_id)
    issued_qty = book.issued_qty - 1
    Books.query.filter_by(id=book_id).update({Books.issued_qty: issued_qty})
    transaction = Transactions.query.filter_by(member_id=member_id, book_id=book_id).first()
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
