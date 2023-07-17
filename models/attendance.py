from models.user import User
from models.event import Event
from models.db import db

# Association tables
attendance = db.Table(
    "attendance",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("event_id", db.Integer, db.ForeignKey("events.id"), primary_key=True),
)
