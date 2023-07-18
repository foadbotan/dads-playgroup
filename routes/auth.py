from flask import session, redirect, render_template, request, Blueprint
from models import User, Event, require_login, require_guest, login

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/login")
@require_guest
def login_form():
    return render_template(
        "forms/login.html.jinja",
        title="Login",
        button_text="Login",
    )


@auth_bp.post("/login")
@require_guest
def login_action():
    email = request.form.get("email")
    password = request.form.get("password")

    user = login(email, password)
    if not user:
        # TODO: flash message
        redirect("/members/login")

    return redirect(f"/members/{user.id}")


@auth_bp.get("/logout")
@require_login
def logout_action():
    session.clear()
    return redirect("/")
