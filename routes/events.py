from flask import Blueprint, render_template, request, redirect
from models import Event

events_bp = Blueprint("events", __name__, url_prefix="/events")


@events_bp.get("/")
def events_list():
    public_events = Event.get_all_public()
    return render_template("events.html.jinja", events=public_events)


@events_bp.get("/<int:event_id>")
def event_detail(event_id=None):
    event = Event.get_by_id(event_id)
    return render_template("event_detail.html.jinja", event=event)


@events_bp.get("/edit/<int:event_id>")
def event_edit_form(event_id=None):
    event = Event.get_by_id(event_id)
    return render_template(
        "forms/event.html.jinja",
        event=event,
        title=f"Edit {event.name}",
        button_text="Save Changes",
    )


@events_bp.post("/edit/<int:event_id>")
def event_edit_action(event_id=None):
    event = Event.get_by_id(event_id)
    event.update(**request.form)
    return redirect(f"/events/{event.id}")
