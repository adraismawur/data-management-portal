from flask import Blueprint

bp_project = Blueprint("project", __file__, url_prefix="/project")

from project import views
