from models.db import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=True)
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
        is_public=True,
    ):
        self.name = name
        self.date = date
        self.time = time
        self.description = description
        self.location = location
        self.creator = creator
        self.attendees = attendees + [creator]
        self.image_url = image_url
        self.is_public = is_public

        db.session.add(self)
        db.session.commit()

        return self

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def f_date(self):
        return self.date.strftime("%a, %d %b")

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
            "is_public": self.is_public,
            "creator_id": self.creator_id,
            "attendees": [attendee.to_dict() for attendee in self.attendees],
        }

    def __repr__(self):
        return f"<Event id={self.id} name={self.name} date={self.date} time={self.time} description={self.description} location={self.location} image_url={self.image_url} is_public={self.is_public} creator_id={self.creator_id} attendees={len(self.attendees)}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_public(cls):
        return cls.query.filter_by(is_public=True).all()
