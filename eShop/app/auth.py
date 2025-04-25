from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from flask_login import current_user
from flask_dance.contrib.google import google
from flask import jsonify

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.")
            return redirect(url_for("auth.register"))

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha256")
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.profile"))  # Adjust this route as needed

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid login credentials.")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("main.profile"))

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))




@auth.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome, {current_user.name or current_user.email}!"

@auth.route("/google_login/callback")
def google_login_callback():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.")
        return redirect(url_for("auth.login"))

    user_info = resp.json()
    email = user_info["email"]
    name = user_info["name"]

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("auth.dashboard"))


@auth.route("/")
def index():
    return render_template("index.html")
