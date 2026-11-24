from flask import render_template

from board import bp_board


@bp_board.route("/")
def overview():
    return render_template("board/overview.html")
