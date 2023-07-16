from flask import Blueprint, render_template
from models import User

members_bp = Blueprint("members", __name__, url_prefix="/members")


@members_bp.get("/")
def members_list():
    members = User.get_all()
    return render_template("members.html.jinja", members=members)


@members_bp.get("/<int:member_id>")
def member_detail(member_id=None):
    member = User.get_by_id(member_id)
    return render_template("member_detail.html.jinja", member=member)
