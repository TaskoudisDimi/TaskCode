from flask_sqlalchemy import SQLAlchemy

# Define db as a global instance (will be initialized by app.py)
db = SQLAlchemy()

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))  # New column for category

class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

class Translation(db.Model):
    __tablename__ = 'translations'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    language_code = db.Column(db.String(10), nullable=False)
    text = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('key', 'language_code'),)