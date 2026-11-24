from flask import render_template

from main import bp_main


@bp_main.route("/")
def home():
    return render_template("main.html")
