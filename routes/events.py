from flask import Blueprint, render_template, request, redirect, session, Response
from models import Event, User, require_admin, require_login, get_logged_in_user


events_bp = Blueprint("events", __name__, url_prefix="/events")


@events_bp.get("/<int:event_id>")
def event_detail(event_id=None):
    event = Event.get(event_id)
    if not event:
        # TODO: flash message
        return redirect("/events")
    return render_template("event.html.jinja", event=event, title=event.name)


@events_bp.get("/create")
@require_admin
def event_create_form():
    return render_template(
        "forms/event.html.jinja",
        title="Create Event",
        button_text="Create Event",
        event=None,
    )


@events_bp.post("/create")
@require_admin
def event_create_action():
    creator = get_logged_in_user()
    event = creator.create_event(**request.form)
    return redirect(f"/events/{event.id}")


@events_bp.get("/edit/<int:event_id>")
@require_admin
def event_edit_form(event_id=None):
    event = Event.get(event_id)
    return render_template(
        "forms/event.html.jinja",
        event=event,
        title=f"Edit {event.name}",
        button_text="Save Changes",
    )


@events_bp.post("/edit/<int:event_id>")
@require_admin
def event_edit_action(event_id=None):
    event = Event.get(event_id)
    event.update(
        name=request.form.get("name"),
        datetime=request.form.get("date") + " " + request.form.get("time"),
        description=request.form.get("description"),
        location=request.form.get("location"),
        image_url=request.form.get("image_url"),
    )
    return redirect(f"/events/{event.id}")


@events_bp.get("/delete/<int:event_id>")
@require_admin
def event_delete_form(event_id=None):
    event = Event.get(event_id)
    return render_template(
        "forms/event.html.jinja",
        event=event,
        title=f"Delete {event.name}",
        button_text="Confirm Delete",
    )


@events_bp.post("/delete/<int:event_id>")
@require_admin
def event_delete_action(event_id=None):
    event = Event.get(event_id)
    event.delete()
    return redirect("/events")


@events_bp.get("/download/<int:event_id>")
def event_download(event_id=None):
    event = Event.get(event_id)
    if not event:
        return redirect("/events")
    return Response(
        event.to_ical(),
        mimetype="text/calendar",
        headers={"Content-Disposition": "attachment;filename=event.ics"},
    )


@events_bp.get("/rsvp/<int:event_id>")
@require_login
def event_rsvp(event_id=None):
    event = Event.get(event_id)
    user = get_logged_in_user()
    if event and user:
        event.rsvp(user)
    return redirect("/events")
