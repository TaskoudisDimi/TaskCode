from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean
from application.database import db  # Import db from database.py

class Template(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    path = Column(String(200), unique=True, nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Template {self.name}>"

class ContactSubmission(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject = Column(String(200))
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<ContactSubmission {self.email} - {self.subject}>"

class Translation(db.Model):
    __tablename__ = 'translations'
    id = db.Column(db.Integer, primary_key=True)
    language_code = db.Column(db.String(10), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Translation {self.key} ({self.language_code})>"

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False)
    service_name = db.Column(db.String(100))
    image_url = db.Column(db.String(255), nullable=False)
    alt_text = db.Column(db.String(255), nullable=False)
    order_index = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<Image {self.image_url} ({self.section})>"

class CompanyDetails(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(50))
    address = Column(String(255))
    city = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    website = Column(String(150))
    hours = Column(String(150))
    linkedin_url = Column(String(255))
    twitter_url = Column(String(255))
    youtube_url = Column(String(255))
    facebook_url = Column(String(255))
    maps_api_key = Column(String(255))

    def __repr__(self):
        return f"<CompanyDetails {self.name}>"