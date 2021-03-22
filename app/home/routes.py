from flask import Blueprint, render_template
from app.models import Transactions, db, Members
from sqlalchemy.sql import func
from sqlalchemy import desc, text

home_bp = Blueprint("home_bp", __name__)


@home_bp.route('/', methods=["GET", "POST"])
@home_bp.route('/home', methods=["GET", "POST"])
def home():
    # result = db.session.query(Transactions.book_id,func.count(Transactions.book_id)).all()
    # print(result)
    # hpc = db.session.query(Transactions, Members, func.sum(Transactions.fee).label("fee_sum"))\
    #     .filter_by(book_status=0, member_id=Members.id)\
    #     .group_by(Transactions.member_id).order_by(desc(func.sum(Transactions.fee)))
    # print(hpc)
    highest_paying_customer = db.session.query('name', 'member_id', 'SUM_1').from_statement(
        text('''select member_id,name,sum(fee) as SUM_1 from transactions as t,
        members as m where book_status=0 and t.member_id=m.id group by member_id order by SUM_1 desc;''')).all()

    most_popular_book = db.session.query('title', 'book_id', 'CNT').from_statement(
        text(''' select title,book_id,count(book_id) as CNT from transactions as t,books as b where t.book_id=b.id 
         group by book_id order by CNT desc;''')).all()

    return render_template("home.html", hpc=highest_paying_customer, mpb=most_popular_book)
