from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()  
login_manager.login_view = 'login'

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Google OAuth setup
    google_bp = make_google_blueprint(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        redirect_url="/google_login/callback",
        scope=["profile", "email"]
    )
    app.register_blueprint(google_bp, url_prefix="/google_login")

    return app