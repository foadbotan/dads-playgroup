import bcrypt
from models.db import db
from models.event import Event


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

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "password":
                key = "password_hash"
                value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
            setattr(self, key, value)

        db.session.add(self)
        db.session.commit()

        return self

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "new_password":
                old_password = kwargs.get("old_password")
                if not old_password or not self.check_password(old_password):
                    # TODO: check if this works
                    raise Exception("Incorrect password")
                key = "password_hash"
                value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
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
