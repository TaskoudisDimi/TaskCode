from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint
from flask_migrate import Migrate  # Add this
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
migrate = Migrate()  # Add this

# Import models
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder="templates")
    print(f"[create_app] Flask root_path: {app.root_path}")

    app.config.from_object("config.Config")
    app.secret_key = os.getenv("SECRET_KEY")

    # Set default theme
    default_theme = os.getenv("THEME", "MyTemplate")
    app.config["ACTIVE_THEME"] = default_theme
    print(f"Using default theme: {default_theme}")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate

    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .shop import shop as shop_blueprint
    app.register_blueprint(shop_blueprint)

    # Google OAuth
    google_bp = make_google_blueprint(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        redirect_url="/google_login/callback",
        scope=["profile", "email"]
    )
    app.register_blueprint(google_bp, url_prefix="/google_login")
    
    return app