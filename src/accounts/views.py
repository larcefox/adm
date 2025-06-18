from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user
from src import db, bcrypt
from src.accounts.models import User, Role
from flask_login import login_required, login_user, logout_user
from .forms import RegisterForm
from .forms import LoginForm


accounts_bp = Blueprint("accounts", __name__, template_folder="templates")

@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", form=form)


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    print(
        url_for("accounts.login"),
        "----------------------------------------------------------------------",
    )
    return redirect(url_for("accounts.login"))


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password.encode("utf8"), request.form["password"]
        ):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)