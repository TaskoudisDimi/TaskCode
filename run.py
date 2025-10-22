from flask import Flask
from sqlalchemy.sql import text
from application.config import Config 
import os
from application.database import db, init_db  

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config.from_object(Config)

    # Initialize database
    init_db(app)

    # Import models after db initialization
    with app.app_context():
        import application.models

    # Register blueprints
    from application.routes import main_bp
    app.register_blueprint(main_bp)

    return app

# Create app instance for WSGI
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database connection failed: {e}")
    app.run(debug=False, host='0.0.0.0', port=5000)