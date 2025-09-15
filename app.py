from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, abort
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
from models import db, Template, ContactSubmission, Translation
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  

db.init_app(app)
migrate = Migrate(app, db)

# Default language (from session, default to 'en' if not set)
def get_user_language():
    return session.get('language', 'en')

# Fetch translation for a given key and language
def get_translation(key, language):
    translation = Translation.query.filter_by(key=key, language_code=language).first()
    return translation.text if translation else f"[{key}]"  # Fallback to key in brackets if not found

def get_translations(language):
    return {
        'tagline': get_translation('tagline', language),
        'services_title': get_translation('services_title', language),
        'contact_title': get_translation('contact_title', language),
        'process_title': get_translation('process_title', language),
        'choose_us_title': get_translation('choose_us_title', language),
        'showcase_title': get_translation('showcase_title', language),
        'pricing_title': get_translation('pricing_title', language),
        'ignite_title': get_translation('ignite_title', language),
        'ignite_description': get_translation('ignite_description', language),
        'ignite_step1': get_translation('ignite_step1', language),
        'ignite_step2': get_translation('ignite_step2', language),
        'ignite_step3': get_translation('ignite_step3', language),
        'form_name': get_translation('form_name', language),
        'form_email': get_translation('form_email', language),
        'form_message': get_translation('form_message', language),
        'form_submit': get_translation('form_submit', language),
        'chat_welcome': get_translation('chat_welcome', language),
        'chat_response': get_translation('chat_response', language),
    }

def categorize_templates(templates):
    categories = set()
    for t in templates:
        if t.category:
            categories.add(t.category.lower())
    categorized = {'all': templates}
    for category in categories:
        categorized[category] = [t for t in templates if t.category and t.category.lower() == category]
    return categorized, list(categories)

@app.route('/set_language', methods=['POST'])
def set_language():
    lang = request.args.get('lang', 'en')
    if lang in ['en', 'el']:
        session['language'] = lang
    return '', 204  # No content response

@app.route('/')
def index():
    language = get_user_language()
    translations = get_translations(language)
    featured_templates = Template.query.all()
    featured_templates_dict = [{"name": t.name, "description": t.description, "path": t.path} for t in featured_templates]
    if 'chat_messages' not in session:
        session['chat_messages'] = [
            {"text": get_translation("chat_welcome", language), "from": "bot"}
        ]
    return render_template('index.html', 
                          featured_templates=featured_templates_dict,
                          chat_messages=session['chat_messages'],
                          translations=translations)

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
    translations = get_translations(language)
    templates = Template.query.all()
    templates_dict = [{"id": t.id, "name": t.name, "description": t.description, "preview": url_for('static', filename='templates/preview_' + t.name.lower().replace(' ', '_') + '.jpg')} for t in templates]
    return render_template('custom_project.html', templates=templates_dict, translations=translations)



@app.route('/templates/<path:template_path>')
def template(template_path):
    language = get_user_language()
    translations = get_translations(language)
    # Check if the template exists in the database
    template_record = Template.query.filter_by(path=template_path).first()
    if not template_record:
        abort(404)
    # Serve the template file from the static/templates directory
    return render_template('template.html', template=template_record, translations=translations)

# Custom route to serve static assets from templates
@app.route('/templates/<path:folder>/<path:filename>')
def serve_template_assets(folder, filename):
    return send_from_directory(f'static/templates/{folder}', filename)

@app.route('/templates', methods=['GET'])
def templates():
    language = get_user_language()
    translations = get_translations(language)
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
                          translations=translations)

@app.route('/sites_eshops_wms', methods=['GET'])
def sites_eshops_wms():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('sites_eshops_wms.html', translations=translations)

@app.route('/logos', methods=['GET'])
def logos():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('logos.html', translations=translations)

@app.route('/AI', methods=['GET'])
def AI():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('AI.html', translations=translations)

@app.route('/prices', methods=['GET'])
def prices():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('prices.html', translations=translations)

@app.route('/about', methods=['GET'])
def about():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('About.html', translations=translations)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    language = get_user_language()
    translations = get_translations(language)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        submission = ContactSubmission(name=name, email=email, subject=subject, message=message)
        db.session.add(submission)
        db.session.commit()
        print(f"Contact Form: {name}, {email}, {subject}, {message}")
    return render_template('contact.html', translations=translations)


@app.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('Newsletter.html', translations=translations)

@app.route('/custom_software', methods=['GET'])
def custom_software():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('Custom_Software.html', translations=translations)

@app.route('/Brand_Identity_Digital_Assets', methods=['GET'])
def Brand_Identity_Digital_Assets():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('Brand_Identity_&_Digital_Assets.html', translations=translations)

@app.route('/Dynamic_Web_Portals', methods=['GET'])
def Dynamic_Web_Portals():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('Dynamic_Web_Portals.html', translations=translations)

@app.route('/eCommerce_solution', methods=['GET'])
def eCommerce_solution():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('eCommerce_solution.html', translations=translations)

@app.route('/Smart_Inventory_Management', methods=['GET'])
def Smart_Inventory_Management():
    language = get_user_language()
    translations = get_translations(language)
    return render_template('Smart_Inventory_Management.html', translations=translations)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)