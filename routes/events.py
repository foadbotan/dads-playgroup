from flask import Blueprint, render_template
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
