from flask import Blueprint, render_template, request, session, redirect, url_for, send_from_directory, abort, flash, current_app
from application.database import db 
from application.models import Template, ContactSubmission 
from application.helpers import (
    get_user_language, 
    get_translation, 
    get_all_translations, 
    categorize_templates, 
    get_company_details, 
    get_all_images,
    format_templates_for_json
)

# Create a Blueprint
main_bp = Blueprint('main', __name__)

def get_common_context():
    """Fetches common data required by most routes."""
    language = get_user_language()
    translations = get_all_translations(language)
    company_details = get_company_details()
    images = get_all_images()
    
    return {
        'language': language, 
        'translations': translations, 
        'company_details': company_details, 
        'images': images
    }

@main_bp.route('/', methods=['GET'])
def index():
    language = request.args.get('lang')
    if language and language in current_app.config['LANGUAGES']:
        session['language'] = language
    elif 'language' not in session:
        session['language'] = 'en'  
        
    context = get_common_context()    

    if 'chat_messages' not in session or any(msg['text'] == '[chat_welcome]' for msg in session.get('chat_messages', [])):
        session['chat_messages'] = [
            {"text": get_translation("chat_welcome", context['language']), "from": "bot"}
        ]
    
    return render_template('index.html', 
                          chat_messages=session['chat_messages'],
                          **context)


@main_bp.route('/set_language/<lang>', methods=['POST'])
def set_language(lang):
    if lang in current_app.config['LANGUAGES']:
        session['language'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/submit_chat', methods=['POST'])
def submit_chat():
    if 'chat_messages' not in session:
        session['chat_messages'] = []
    
    language = get_user_language()
    user_message = request.form.get('chat_input', '').strip()
    
    if user_message:
        session['chat_messages'].append({"text": user_message, "from": "user"})
        session['chat_messages'].append({"text": get_translation("chat_response", language), "from": "bot"})

    return redirect(url_for('main.index')) 

@main_bp.route('/custom_project')
def custom_project():
    context = get_common_context()
    templates = Template.query.all() 
    templates_dict = format_templates_for_json(templates)
    
    return render_template('custom_project.html', 
                          templates=templates_dict, 
                          **context)

@main_bp.route('/templates/<path:template_path>')
def template(template_path):
    context = get_common_context()
    template_record = Template.query.filter_by(path=template_path).first()
    
    if not template_record:
        abort(404)
        
    return render_template('template.html', 
                          template=template_record, 
                          **context)

@main_bp.route('/templates/<path:folder>/<path:filename>')
def serve_template_assets(folder, filename):
    return send_from_directory(f'static/templates/{folder}', filename)

@main_bp.route('/templates', methods=['GET'])
def templates():
    context = get_common_context()
    all_templates = Template.query.all()
    
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', 'all').lower()
    
    templates_filtered = all_templates
    
    if search_query:
        templates_filtered = [t for t in templates_filtered if search_query in t.name.lower() or search_query in t.description.lower()]
    
    if category_filter != 'all':
        templates_filtered = [t for t in templates_filtered if t.category and t.category.lower() == category_filter]

    categorized_templates, categories = categorize_templates(templates_filtered)
    
    return render_template('templates.html', 
                          categorized_templates=categorized_templates, 
                          categories=categories,
                          **context)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    context = get_common_context()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        submission = ContactSubmission(name=name, email=email, subject=subject, message=message)
        db.session.add(submission)
        db.session.commit()
        
        flash(context['translations'].get('contact_success_message', 'Your message has been sent successfully!'), 'success')
        return redirect(url_for('main.contact'))
        
    return render_template('contact.html', **context)

@main_bp.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    context = get_common_context()
    
    if request.method == 'POST':        
        flash(context['translations'].get('newsletter_success_message', 'Thank you for subscribing! We\'ve sent a confirmation email.'), 'success')
        return render_template('Newsletter.html', message="success", **context)
        
    return render_template('Newsletter.html', **context)

@main_bp.route('/sites_eshops_wms', methods=['GET'])
def sites_eshops_wms():
    return render_template('sites_eshops_wms.html', **get_common_context())

@main_bp.route('/logos', methods=['GET'])
def logos():
    return render_template('logos.html', **get_common_context())

@main_bp.route('/AI', methods=['GET'])
def AI():
    return render_template('AI.html', **get_common_context())

@main_bp.route('/prices', methods=['GET'])
def prices():
    return render_template('prices.html', **get_common_context())

@main_bp.route('/about', methods=['GET'])
def about():
    return render_template('About.html', **get_common_context())

@main_bp.route('/custom_software', methods=['GET'])
def custom_software():
    return render_template('Custom_Software.html', **get_common_context())

@main_bp.route('/Brand_Identity_Digital_Assets', methods=['GET'])
def Brand_Identity_Digital_Assets():
    return render_template('Brand_Identity_&_Digital_Assets.html', **get_common_context())

@main_bp.route('/Dynamic_Web_Portals', methods=['GET'])
def Dynamic_Web_Portals():
    return render_template('Dynamic_Web_Portals.html', **get_common_context())

@main_bp.route('/eCommerce_solution', methods=['GET'])
def eCommerce_solution():
    return render_template('eCommerce_solution.html', **get_common_context())

@main_bp.route('/Smart_Inventory_Management', methods=['GET'])
def Smart_Inventory_Management():
    return render_template('Smart_Inventory_Management.html', **get_common_context())