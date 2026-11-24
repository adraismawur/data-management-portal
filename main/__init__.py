from flask import Blueprint

bp_main = Blueprint("main", __file__)

from main import views
