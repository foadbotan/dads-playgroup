from flask import session, redirect, render_template, request, Blueprint
from models import User, Event, require_login, require_guest

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/login")
@require_guest
def login_form():
    return render_template(
        "forms/login.html.jinja", title="Login", button_text="Login", member=None
    )


@auth_bp.post("/login")
@require_guest
def login_action():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)
    if not user or not user.check_password(password):
        redirect("/members/login")

    session["user"] = {
        "id": user.id,
        "name": user.name,
        "is_admin": user.is_admin,
    }
    return redirect(f"/members/{user.id}")


@auth_bp.get("/logout")
@require_login
def logout_action():
    session.clear()
    return redirect("/")
