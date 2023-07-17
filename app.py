from flask import Flask, render_template
import os
from dotenv import load_dotenv
from models import db, User, Event
from routes import events, members, auth


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PORT"] = os.getenv("PORT", default=5000)

    db.init_app(app)

    app.register_blueprint(events.events_bp)
    app.register_blueprint(members.members_bp)
    app.register_blueprint(auth.auth_bp)

    @app.route("/")
    def index():
        return render_template("index.html.jinja")

    return app


if __name__ == "__main__":
    from seed_db import seed_db

    app = create_app()
    with app.app_context():
        seed_db(db)

    app.run(debug=True)
