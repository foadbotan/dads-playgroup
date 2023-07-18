from models.db import db
from datetime import datetime


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
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
        self.date = date
        self.time = time
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

    def is_upcoming(self):
        return self.date > datetime.now().date()


    @property
    def f_date(self):
        return self.date.strftime("%a, %d %b %Y")

    @property
    def f_time(self):
        return self.time.strftime("%H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "description": self.description,
            "location": self.location,
            "image_url": self.image_url,
            "creator_id": self.creator_id,
            "attendees": [attendee.to_dict() for attendee in self.attendees],
        }

    def __repr__(self):
        return f"<Event id={self.id} name={self.name} date={self.date} time={self.time} description={self.description} location={self.location} image_url={self.image_url} creator_id={self.creator_id} attendees={len(self.attendees)}>"

    @classmethod
    def get(cls, id):
        return cls.query.get(id)


    @classmethod
    def upcoming_events(cls):
        return cls.query.filter(cls.date > datetime.now().date()).order_by(cls.date).all()

    @classmethod
    def past_events(cls):
        return cls.query.filter(cls.date < datetime.now().date()).order_by(cls.date.desc()).limit(3).all()