from models.db import db
from datetime import datetime, timedelta
import arrow
from ics import Calendar, Event as IcsEvent


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creator = db.relationship("User", back_populates="created")
    attendees = db.relationship(
        "User", secondary="attendance", back_populates="attending"
    )

    def __init__(
        self,
        name,
        date,
        time,
        description,
        location,
        creator,
        attendees=[],
        image_url=None,
    ):
        self.name = name
        self.datetime = f"{date} {time}"
        self.description = description
        self.location = location
        self.creator = creator
        self.attendees = attendees + [creator]
        self.image_url = image_url

        db.session.add(self)
        db.session.commit()

        return self

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key not in Event.__table__.columns:
                raise Exception(f"Invalid key '{key}'")
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_ical(self):
        cal = Calendar()
        event = IcsEvent(
            name=self.name,
            begin=self.datetime,
            end=self.datetime + timedelta(hours=2),
            description=self.description,
            location=self.location,
            url=f"https://dads-playgroup.onrender.com/events/{self.id}",
        )
        cal.events.add(event)
        return cal

    def relative_date(self):
        return arrow.get(self.datetime).humanize()

    def attendee_ids(self):
        return [attendee.id for attendee in self.attendees]

    def rsvp(self, user):
        if user in self.attendees:
            self.attendees.remove(user)
        else:
            self.attendees.append(user)
        db.session.commit()

    def is_upcoming(self):
        return self.datetime > datetime.now()

    @property
    def date(self):
        return self.datetime.strftime("%a, %d %b")

    @property
    def time(self):
        return self.datetime.strftime("%H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime,
            "description": self.description,
            "location": self.location,
            "image_url": self.image_url,
            "creator_id": self.creator_id,
            "attendees": [attendee.to_dict() for attendee in self.attendees],
        }

    def __repr__(self):
        return f"<Event id={self.id} name={self.name} datetime={datetime} description={self.description} location={self.location} image_url={self.image_url} creator_id={self.creator_id} attendees={len(self.attendees)}>"

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def upcoming_events(cls):
        return (
            cls.query.filter(cls.datetime > datetime.now()).order_by(cls.datetime).all()
        )

    @classmethod
    def past_events(cls):
        return (
            cls.query.filter(cls.datetime < datetime.now())
            .order_by(cls.datetime.desc())
            .limit(3)
            .all()
        )
