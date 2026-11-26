from flask import Blueprint

bp_auth = Blueprint("auth", __file__, url_prefix="/auth")

from auth import views
