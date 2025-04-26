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
        # Hash the password using a secure method (pbkdf2:sha256)
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        # Create user with password if they are not using Google
        new_user = User(
            email=email,
            name=name,
            password=hashed_password,
            google_id=None  # This is NULL for manual users
        )
        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("auth.dashboard"))  # Adjust this route as needed

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check for manual email/password login
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("auth.dashboard"))
            else:
                flash("Invalid login credentials.")
        else:
            flash("Email does not exist.")

        return redirect(url_for("auth.login"))

    return render_template("login.html")



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))




@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

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
    google_id = user_info["id"]  # Get Google ID from response

    # Check if user already exists, otherwise create a new user
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            email=email,
            name=name,
            google_id=google_id,  # Set Google ID for this user
            password=None  # No password required for Google users
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("auth.dashboard"))



@auth.route("/")
def index():
    return render_template("index.html")
