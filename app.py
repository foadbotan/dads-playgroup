from flask import Flask, render_template
import os
from dotenv import load_dotenv
from models import db, Event
from routes import events, members, auth


def create_app():
    app = Flask(__name__)
    load_dotenv()

    # TODO: move to config file
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PORT"] = os.getenv("PORT", default=5000)

    db.init_app(app)

    app.register_blueprint(events.events_bp)
    app.register_blueprint(members.members_bp)
    app.register_blueprint(auth.auth_bp)

    @app.route("/events/")
    @app.route("/")
    def index():
        upcoming_events = Event.upcoming_events()
        past_events = Event.past_events()

        return render_template(
            "index.html.jinja", upcoming_events=upcoming_events, past_events=past_events
        )

    return app


if __name__ == "__main__":
    # TODO: remove this
    from seed_db import seed_db

    app = create_app()
    with app.app_context():
        seed_db(db)

    app.run(debug=True)
