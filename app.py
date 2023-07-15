from flask import Flask, render_template
import os
from dotenv import load_dotenv
from models import db, User, Event


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PORT"] = os.getenv("PORT", default=5000)

    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html.jinja")

    @app.route("/events")
    def events_list():
        public_events = Event.get_all_public()
        return render_template("events.html.jinja", events=public_events)

    @app.route("/events/<int:event_id>")
    def event_detail(event_id=None):
        event = Event.get_by_id(event_id)
        return render_template("event_detail.html.jinja", event=event)

    @app.route("/members")
    def members_list():
        members = User.get_all()
        return render_template("members.html.jinja", members=members)

    @app.route("/members/<int:member_id>")
    def member_detail(member_id=None):
        member = User.get_by_id(member_id)
        return render_template("member_detail.html.jinja", member=member)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
