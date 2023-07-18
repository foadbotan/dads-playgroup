from flask import session, redirect
from .user import User
from .event import Event


def get_logged_in_user():
    if not session.get("user"):
        return None
    user_id = session.get("user").get("id")
    user = User.get(id=user_id)
    return user


def require_login(func):
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect("/login")
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def require_admin(func):
    @require_login
    def wrapper(*args, **kwargs):
        if not session.get("user").get("is_admin"):
            user_id = session.get("user").get("id")
            return redirect(f"/members/{user_id}")
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def require_guest(func):
    def wrapper(*args, **kwargs):
        if session.get("user"):
            return redirect("/")
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def require_public_event(func):
    def wrapper(*args, **kwargs):
        event_id = kwargs.get("event_id")
        event = Event.get(event_id)
        if not event.is_public and not session.get("user"):
            return redirect("/login")
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def login(email, password):
    user = User.get(email=email)
    if not user or not user.check_password(password):
        return None

    session["user"] = {
        "id": user.id,
        "name": user.name,
        "is_admin": user.is_admin,
    }
    return user
