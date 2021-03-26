from flask import Blueprint, render_template, flash, redirect, url_for
from app.members.forms import MemberForm, SearchForm
from app.models import Members
from app.models import db
import re

members_bp = Blueprint("members_bp", __name__)


def search(pattern, data):
    result = []
    for member in data:
        temp_1 = re.search(pattern, str(member.id))
        temp_2 = re.search(pattern, member.name)
        temp_3 = re.search(pattern, str(member.contact))
        if temp_1 or temp_2 or temp_3:
            result.append(member)
    return result


@members_bp.route("/search_member", methods=["GET", "POST"])
def search_member():
    form = SearchForm()
    if form.is_submitted():
        pattern = form.search_title.data
        members = Members.query.all()
        result = search(pattern, members)
        if result:
            flash("Member Found !")
            return render_template("found_member.html", result=result)
        else:
            flash("Sorry! No such member found")
            return render_template("found.html")


@members_bp.route("/get_members", methods=["GET", "POST"])
def get_members():
    form = SearchForm()
    data = Members.query.all()
    return render_template("members.html", data=data, form=form)


@members_bp.route("/add_member", methods=["GET", "POST"])
def add_member():
    form = MemberForm()
    if form.validate_on_submit():
        data = Members(name=form.member_name.data, contact=form.contact_no.data, email=form.email.data,
                       dob=form.dob.data)
        db.session.add(data)
        db.session.commit()
        flash("Member added successfully")
    return render_template("add_member.html", form=form)


@members_bp.route("/edit_member/<int:id>", methods=["GET", "POST"])
def edit_member(id):
    form = MemberForm()
    member = Members.query.get_or_404(id)

    if form.validate_on_submit():
        Members.query.filter_by(id=id).update(
            {Members.name: form.member_name.data, Members.contact: form.contact_no.data,
             Members.email: form.email.data, Members.dob: form.dob.data})
        db.session.commit()
        flash("member details edited successfully")
        return redirect(url_for('members_bp.edit_member', id=member.id))

    form.member_name.default = member.name
    form.contact_no.default = member.contact
    form.email.default = member.email
    form.dob.default = member.dob
    form.process()
    return render_template("add_member.html", form=form, member=member)


@members_bp.route("/delete_member/<int:id>", methods=["GET", "POST"])
def delete_member(id):
    member = Members.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash("Member deleted Successfully !")
    return redirect(url_for('members_bp.get_members'))
