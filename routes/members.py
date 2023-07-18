from flask import Blueprint, render_template, request, redirect, session
from models import User, Event, require_login, require_guest, require_admin

members_bp = Blueprint("members", __name__, url_prefix="/members")


@members_bp.before_request
@require_login  # Protects all /members endpoints with require_login
def before_request():
    pass


@members_bp.get("/")
def members_list():
    members = User.get_all()
    return render_template("members.html.jinja", members=members)


@members_bp.get("/<int:member_id>")
def member_detail(member_id=None):
    user = User.get(id=member_id)
    if not user:
        # TODO: flash message
        return redirect("/members")
    return render_template("member_detail.html.jinja", member=user)
