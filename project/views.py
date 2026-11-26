from flask import redirect, render_template, request, url_for

from flask_login import current_user
from sqlalchemy import Select, insert, select

from models import User, db

from forms.project import ProjectForm
from models import Project
from project import bp_project


@bp_project.route("/new", methods=["GET", "POST"])
def new():
    form = ProjectForm(request.form)

    if request.method == "POST":

        project = Project.from_form(form)

        project.users.append(current_user)

        db.session.add(project)

        db.session.commit()

        return redirect(url_for("project.view", project_id=project.id))

    return render_template("project/new.html", form=form)


@bp_project.route("/view/<project_id>")
def view(project_id: int):
    statement = select(Project).where(Project.id == project_id)

    project = db.session.scalar(statement)

    if not project:
        return redirect(url_for("project.list"))

    return render_template("project/view.html", project=project)


@bp_project.route("/list")
def list():
    statement = Select(Project).where(Project.users.any(User.id == current_user.id))

    projects = db.session.scalars(statement).all()

    return render_template("project/list.html", projects=projects, asd=statement)


@bp_project.route("/form/new/<form_type>")
def form_new(form_type: str):
    return render_template("project/form_new.html")


@bp_project.route("/form/view/<form_id>")
def form_view(form_id: int):
    return render_template("project/form_view.html")
