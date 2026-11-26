from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import Select

from models import TestLogin, User, db

from auth import bp_auth
from forms.auth import TestLoginForm


@bp_auth.route("/test_login", methods=["GET", "POST"])
def test_login():

    form = TestLoginForm(request.form)

    if request.method == "POST":
        statement = (
            Select(User)
            .join(TestLogin, TestLogin.id == User.id)
            .where(TestLogin.user_name == form.user_name.data)
        )

        user = db.session.scalar(statement)

        if not user:
            flash("Login failed", "error")
            return render_template("auth/test_login.html", form=form)

        login_user(user)

        flash(f"Logged in as {current_user.name}")

        return redirect(url_for("main.home"))

    return render_template("auth/test_login.html", form=form)


@bp_auth.route("/logout")
def log_out():
    logout_user()
    return redirect(url_for("main.home"))
