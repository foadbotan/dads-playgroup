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

    db.init_app(app)

    @app.route("/")
    def index():
        users = User.get_all()
        print(users)
        return render_template("index.html.jinja", users=users)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=os.getenv("PORT", default=5000))
