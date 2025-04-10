from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

# Import models early to avoid circular imports later
from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder="templates")  # 👈 explicitly tell Flask where templates are

    app.config.from_object("config.Config")

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Register authentication blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Register Google OAuth blueprint
    google_bp = make_google_blueprint(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        redirect_url="/google_login/callback",
        scope=["profile", "email"]
    )
    app.register_blueprint(google_bp, url_prefix="/google_login")

    return app
