from flask import Blueprint, render_template, make_response
from app.models import Transactions, db, Members
from sqlalchemy.sql import func
from sqlalchemy import desc, text
import pdfkit

home_bp = Blueprint("home_bp", __name__)


@home_bp.route('/', methods=["GET", "POST"])
@home_bp.route('/home', methods=["GET", "POST"])
def home():
    highest_paying_customer = db.session.query('name', 'member_id', 'SUM_1').from_statement(
        text('''select member_id,name,sum(fee) as SUM_1 from transactions as t,
        members as m where book_status=0 and t.member_id=m.id group by member_id order by SUM_1 desc LIMIT 5;''')).all()

    most_popular_book = db.session.query('title', 'book_id', 'CNT', 'total_qty', 'issued_qty').from_statement(
        text(''' select total_qty,issued_qty,title,book_id,count(book_id) as CNT from transactions as t,books as b where
         t.book_id=b.id 
         group by book_id order by CNT desc LIMIT 5;''')).all()

    earning_per_month = db.session.query('month', 'total_sum').from_statement(
        text('''select extract(MONTH from return_date) as month,
        sum(fee) as total_sum from transactions where book_status=0 group by month;''')).all()

    labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]

    values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for each_month in earning_per_month:
        values.insert(each_month[0] - 1, each_month[1])

    max_value = max(values)

    return render_template("home.html", hpc=highest_paying_customer, mpb=most_popular_book,
                           max=max_value, labels=labels, values=values)


@home_bp.route('/get_report', methods=["GET", "POST"])
def get_report():
    path_wk_lib = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wk_lib)
    pdf = pdfkit.from_url('http://127.0.0.1:5000/home', False, configuration=config)

    response = make_response(pdf)

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

    return response
