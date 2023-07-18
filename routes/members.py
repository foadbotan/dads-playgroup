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


@members_bp.get("/edit/<int:member_id>")
@require_admin
def member_edit_form(member_id=None):
    member = User.get(id=member_id)
    if not member:
        # TODO: flash message
        return redirect("/members")
    return render_template(
        "forms/member.html.jinja",
        member=member,
        title="Edit Member",
        button_text="Update",
    )


@members_bp.post("/edit/<int:member_id>")
@require_admin
def member_edit_action(member_id=None):
    member = User.get(id=member_id)
    if not member:
        # TODO: flash message
        return redirect("/members")
    member.update(
        name=request.form["name"],
        email=request.form["email"],
        is_admin=request.form.get("is_admin"),
    )
    return redirect(f"/members/{member_id}")
