# models.py
def init_models(db):
    class Template(db.Model):
        __tablename__ = 'templates'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text, nullable=False)
        path = db.Column(db.String(255), nullable=False)
        category = db.Column(db.String(50))

    class ContactSubmission(db.Model):
        __tablename__ = 'contact_submissions'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)
        subject = db.Column(db.String(200), nullable=False)
        message = db.Column(db.Text, nullable=False)

    class Translation(db.Model):
        __tablename__ = 'translations'
        id = db.Column(db.Integer, primary_key=True)
        key = db.Column(db.String(100), nullable=False)
        language_code = db.Column(db.String(10), nullable=False)
        text = db.Column(db.Text, nullable=False)

    class Image(db.Model):
        __tablename__ = 'images'
        id = db.Column(db.Integer, primary_key=True)
        section = db.Column(db.String(100), nullable=False)
        service_name = db.Column(db.String(100))
        image_url = db.Column(db.String(255), nullable=False)
        alt_text = db.Column(db.String(255), nullable=False)
        order_index = db.Column(db.Integer, nullable=False)

    class CompanyDetails(db.Model):
        __tablename__ = 'company_details'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)
        phone = db.Column(db.String(20))
        address = db.Column(db.String(255))
        city = db.Column(db.String(100))
        country = db.Column(db.String(100))
        postal_code = db.Column(db.String(20))
        website = db.Column(db.String(255))
        hours = db.Column(db.String(100))  # Added for business hours
        linkedin_url = db.Column(db.String(255))  # Added for LinkedIn
        twitter_url = db.Column(db.String(255))  # Added for Twitter
        youtube_url = db.Column(db.String(255))  # Added for YouTube
        facebook_url = db.Column(db.String(255))  # Added for Facebook
        maps_api_key = db.Column(db.String(100))  # New field for the API key
        created_at = db.Column(db.DateTime, server_default=db.func.now())

    return Template, ContactSubmission, Translation, Image, CompanyDetails