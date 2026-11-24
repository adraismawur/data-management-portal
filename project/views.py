from flask import render_template

from project import bp_project


@bp_project.route("/new", methods=["GET", "POST"])
def new():
    return render_template("project/new.html")


@bp_project.route("/list")
def list():
    return render_template("project/list.html")
