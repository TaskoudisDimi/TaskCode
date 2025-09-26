from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, abort, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import and initialize models after db is set up
from models import init_models
Template, ContactSubmission, Translation, Image, CompanyDetails = init_models(db)

# Default language (from session, default to 'en' if not set)
def get_user_language():
    return session.get('language', 'en')

# Fetch translation for a given key and language (used as a fallback in templates)
def get_translation(key, language):
    translation = Translation.query.filter_by(key=key, language_code=language).first()
    return translation.text if translation else f"[{key}]"  

def categorize_templates(templates):
    categories = set()
    for t in templates:
        if t.category:
            categories.add(t.category.lower())
    categorized = {'all': templates}
    for category in categories:
        categorized[category] = [t for t in templates if t.category and t.category.lower() == category]
    return categorized, list(categories)

def get_company_details():
    details = CompanyDetails.query.first()
    if details:
        return {
            'name': details.name,
            'email': details.email,
            'phone': details.phone,
            'address': details.address,
            'city': details.city,
            'country': details.country,
            'postal_code': details.postal_code,
            'website': details.website,
            'hours': details.hours,
            'linkedin_url': details.linkedin_url,
            'twitter_url': details.twitter_url,
            'youtube_url': details.youtube_url,
            'facebook_url': details.facebook_url,
            'maps_api_key': details.maps_api_key
        }
    return {}

def get_all_images():
    """Fetches and structures all image data from the database."""
    images = {'vision': [], 'services': {}, 'solutions': {}, 'logo': []}
    image_records = Image.query.order_by(Image.order_index).all() 
    for img in image_records:
        section = img.section
        service = img.service_name
        
        # Ensure the section key exists in the images dictionary
        if section not in images:
            images[section] = {} if service else [] # Initialize as dict if it's a service, else a list

        if service:
            # If it's a service image, ensure the service_name key exists within the section
            if service not in images[section]:
                images[section][service] = []
            images[section][service].append({'image_url': img.image_url, 'alt_text': img.alt_text})
        else:
            # If it's a general section image, append to the list
            images[section].append({'image_url': img.image_url, 'alt_text': img.alt_text})
    
    return images


@app.route('/', methods=['GET'])
def index():
    language = request.args.get('lang', session.get('language', 'en'))
    session['language'] = language

    # Fetch translations using SQLAlchemy
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    
    # Fetch company details
    company_details = get_company_details()

    # Fetch images using the helper function
    images = get_all_images()

    if 'chat_messages' not in session:
        session['chat_messages'] = [
            {"text": get_translation("chat_welcome", language), "from": "bot"}
        ]
    return render_template('index.html', 
                          translations=translations,
                          images=images,
                          company_details=company_details,
                          chat_messages=session['chat_messages'])


@app.route('/set_language/<lang>', methods=['POST'])
def set_language(lang):
    if lang in ['en', 'el']:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/submit_chat', methods=['POST'])
def submit_chat():
    if 'chat_messages' not in session:
        session['chat_messages'] = []
    
    language = get_user_language()
    user_message = request.form.get('chat_input', '').strip()
    if user_message:
        session['chat_messages'].append({"text": user_message, "from": "user"})
        session['chat_messages'].append({"text": get_translation("chat_response", language), "from": "bot"})

    return redirect(url_for('index'))

@app.route('/custom_project')
def custom_project():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    templates = Template.query.all()
    templates_dict = [{"id": t.id, "name": t.name, "description": t.description, "preview": url_for('static', filename='templates/preview_' + t.name.lower().replace(' ', '_') + '.jpg')} for t in templates]
    return render_template('custom_project.html', templates=templates_dict, translations=translations, company_details=company_details, images=images)


@app.route('/templates/<path:template_path>')
def template(template_path):
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    template_record = Template.query.filter_by(path=template_path).first()
    if not template_record:
        abort(404)
    return render_template('template.html', template=template_record, translations=translations, company_details=company_details, images=images)

@app.route('/templates/<path:folder>/<path:filename>')
def serve_template_assets(folder, filename):
    return send_from_directory(f'static/templates/{folder}', filename)

@app.route('/templates', methods=['GET'])
def templates():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    templates = Template.query.all()
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', 'all').lower()

    if search_query:
        templates = [t for t in templates if search_query in t.name.lower() or search_query in t.description.lower()]
    if category_filter != 'all':
        templates = [t for t in templates if t.category and t.category.lower() == category_filter]

    categorized_templates, categories = categorize_templates(templates)
    return render_template('templates.html', 
                          categorized_templates=categorized_templates, 
                          categories=categories,
                          translations=translations,
                          company_details=company_details,
                          images=images)

@app.route('/sites_eshops_wms', methods=['GET'])
def sites_eshops_wms():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('sites_eshops_wms.html', translations=translations, company_details=company_details, images=images)

@app.route('/logos', methods=['GET'])
def logos():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('logos.html', translations=translations, company_details=company_details, images=images)

@app.route('/AI', methods=['GET'])
def AI():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('AI.html', translations=translations, company_details=company_details, images=images)

@app.route('/prices', methods=['GET'])
def prices():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('prices.html', translations=translations, company_details=company_details, images=images)

@app.route('/about', methods=['GET'])
def about():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('About.html', translations=translations, company_details=company_details, images=images)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        submission = ContactSubmission(name=name, email=email, subject=subject, message=message)
        db.session.add(submission)
        db.session.commit()
        flash('Your message has been sent successfully!', 'success')
        print(f"Contact Form: {name}, {email}, {subject}, {message}")
        return redirect(url_for('contact'))
    return render_template('contact.html', translations=translations, company_details=company_details, images=images)

@app.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    if request.method == 'POST':
        email = request.form.get('email')
        # Here you would typically save the email to a database
        print(f"Newsletter subscription email: {email}")
        flash('Thank you for subscribing! We\'ve sent a confirmation email.', 'success')
        return render_template('Newsletter.html', translations=translations, company_details=company_details, images=images, message="success")
    return render_template('Newsletter.html', translations=translations, company_details=company_details, images=images)

@app.route('/custom_software', methods=['GET'])
def custom_software():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('Custom_Software.html', translations=translations, company_details=company_details, images=images)

@app.route('/Brand_Identity_Digital_Assets', methods=['GET'])
def Brand_Identity_Digital_Assets():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('Brand_Identity_&_Digital_Assets.html', translations=translations, company_details=company_details, images=images)

@app.route('/Dynamic_Web_Portals', methods=['GET'])
def Dynamic_Web_Portals():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('Dynamic_Web_Portals.html', translations=translations, company_details=company_details, images=images)

@app.route('/eCommerce_solution', methods=['GET'])
def eCommerce_solution():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('eCommerce_solution.html', translations=translations, company_details=company_details, images=images)

@app.route('/Smart_Inventory_Management', methods=['GET'])
def Smart_Inventory_Management():
    language = get_user_language()
    translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
    company_details = get_company_details()
    images = get_all_images() # Fetch images
    return render_template('Smart_Inventory_Management.html', translations=translations, company_details=company_details, images=images)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)