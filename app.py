from flask import Flask

from flask_login import LoginManager
from sqlalchemy import Select

from main import bp_main
from project import bp_project
from board import bp_board
from auth import bp_auth

from models import User, db


def register_blueprints(app: Flask) -> Flask:
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_project)
    app.register_blueprint(bp_board)
    app.register_blueprint(bp_auth)

    return app


app = Flask(__name__)
app.config.from_object("config")
app = register_blueprints(app)

db.init_app(app)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> User:
    statement = Select(User).where(User.id == int(user_id))

    return db.session.scalar(statement)


with app.app_context():
    db.create_all()
    login_manager.init_app(app)
