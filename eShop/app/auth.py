from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db


auth = Blueprint("auth", __name__)

@auth.route("/")
@auth.route("/index")
def index():
    return render_template("index.html")

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/register")
def register():
    return render_template("register.html")

@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.index"))