import bcrypt
from models.db import db
from models.event import Event

# TODO: Add roles 'pending_approval', 'member', 'admin', 'super_admin'


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

    def __init__(self, name, email, password, is_admin=False):
        self.name = name
        self.email = email
        self.password_hash = User.hash_password(password)
        self.is_admin = is_admin

        db.session.add(self)
        db.session.commit()

        return self

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key not in User.__table__.columns:
                # TODO: check if this works
                raise Exception(f"Invalid key '{key}'")
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email} is_admin={self.is_admin} attending={len(self.attending)} created={len(self.created)}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
            "attending": [event.to_dict() for event in self.attending],
            "created": [event.to_dict() for event in self.created],
        }

    def create_event(self, **kwargs):
        event = Event(creator=self, **kwargs)
        db.session.add(event)
        db.session.commit()
        return event

    def upcoming_events(self):
        return [event for event in self.attending if event.is_upcoming()]

    def past_events(self):
        return [event for event in self.attending if not event.is_upcoming()]

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and user.validate_password(password):
            return user
        return False

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
