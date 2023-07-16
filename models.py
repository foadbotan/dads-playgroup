from flask_sqlalchemy import SQLAlchemy
import bcrypt

# TODO: Create Location table and add relationship to Event

db = SQLAlchemy()

# Association tables
attendance = db.Table(
    "attendance",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("event_id", db.Integer, db.ForeignKey("events.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    attending = db.relationship(
        "Event", secondary="attendance", back_populates="attendees"
    )
    created = db.relationship("Event", back_populates="creator")

    def update(self, name, email, password, is_admin):
        self.name = name
        self.email = email
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.is_admin = is_admin
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def validate_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email}>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

    def create_event(
        self,
        name,
        date,
        description,
        location,
        attendees=[],
        image_url=None,
        is_public=True,
    ):
        event = Event.create(
            name=name,
            date=date,
            description=description,
            location=location,
            creator=self,
            attendees=attendees,
            image_url=image_url,
            is_public=is_public,
        )
        return event

    @classmethod
    def create(cls, name, email, password, is_admin=False):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = cls(
            name=name, email=email, password_hash=password_hash, is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and user.validate_password(password):
            return user
        return False

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_admins(cls):
        return cls.query.filter_by(is_admin=True).all()


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creator = db.relationship("User", back_populates="created")
    attendees = db.relationship(
        "User", secondary="attendance", back_populates="attending"
    )

    def update(self, name, date, description, location, image_url, is_public):
        self.name = name
        self.date = date
        self.description = description
        self.location = location
        self.image_url = image_url
        self.is_public = is_public
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "description": self.description,
            "location": self.location,
            "image_url": self.image_url,
            "is_public": self.is_public,
            "creator_id": self.creator_id,
            "attendees": [attendee.to_dict() for attendee in self.attendees],
        }

    def __repr__(self):
        return f"<Event id={self.id} name={self.name} date={self.date} location={self.location} is_public={self.is_public} creator_id={self.creator_id}>"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_public(cls):
        return cls.query.filter_by(is_public=True).all()

    @classmethod
    def create(
        cls,
        name,
        date,
        description,
        location,
        creator,
        attendees=[],
        image_url=None,
        is_public=False,
    ):
        event = cls(
            name=name,
            date=date,
            description=description,
            location=location,
            image_url=image_url,
            is_public=is_public,
            creator=creator,
            attendees=attendees + [creator],
        )
        db.session.add(event)
        db.session.commit()
        return event
