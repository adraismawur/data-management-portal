from flask import Blueprint

bp_form = Blueprint("form", __file__, url_prefix="/form")

from form import views
