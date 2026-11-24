from flask import Blueprint

bp_board = Blueprint("board", __file__, url_prefix="/board")

from board import views
