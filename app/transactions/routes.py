from flask import Blueprint, render_template, flash, redirect, url_for
from sqlalchemy.sql import func
from app.transactions.forms import TransactionForm
from app.models import Transactions, Books, Members
from app.models import db
from datetime import datetime
from sqlalchemy import desc, text

transactions_bp = Blueprint("transactions_bp", __name__)

Charge = 10
Late_Charge = Charge + 5


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
            return render_template("add_transaction.html", form=form)
        else:
            flash("Sorry! book cannot be issued due to low stock  or member not found!")
            return render_template("add_transaction.html", form=form)
    form.book_id.default = book.id
    form.process()
    return render_template("add_transaction.html", form=form)


@transactions_bp.route("/view_transaction/<int:id>", methods=["GET", "POST"])
def view_transaction(id):
    transactions = Transactions.query.filter_by(member_id=id).all()
    return render_template("view_transaction.html", transactions=transactions)


@transactions_bp.route("/transactions", methods=["GET", "POST"])
def all_transactions():
    transactions = Transactions.query.all()
    return render_template("transactions.html", transactions=transactions)


@transactions_bp.route("/get_defaulters", methods=["GET", "POST"])
def get_defaulters():
    curr_dt = datetime.now()
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

    return render_template("transactions.html", transactions=final_list)


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
