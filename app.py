from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from main import bp_main
from form import bp_form
from project import bp_project
from board import bp_board


def register_blueprints(app: Flask) -> Flask:
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_form)
    app.register_blueprint(bp_project)
    app.register_blueprint(bp_board)

    return app


app = Flask(__name__)
app.config.from_object("config")
app = register_blueprints(app)
db: SQLAlchemy = SQLAlchemy(app)


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()
