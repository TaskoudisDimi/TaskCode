from flask import session, url_for, current_app 
from sqlalchemy.orm import class_mapper
from application.models import Template, ContactSubmission, Translation, Image, CompanyDetails
from application.database import db  
from sqlalchemy.exc import SQLAlchemyError

def get_user_language():
    """Returns the user's selected language from the session, defaulting to 'en'."""
    return session.get('language', current_app.config.get('LANGUAGES')[0]) 

def get_translation(key, language):
    with current_app.app_context():        
        translations = get_all_translations(language)        
        return translations.get(key, key)

def get_all_translations(language):
    with current_app.app_context():        
        try:
            translations = {t.key: t.text for t in Translation.query.filter_by(language_code=language).all()}
            return translations
        except SQLAlchemyError as e:
            return {}
        except Exception as e:
            return {}

def categorize_templates(templates):
    """Categorizes a list of Template objects."""
    categories = set()
    for t in templates:
        if t.category:
            categories.add(t.category.lower())
    
    categorized = {'all': templates}
    for category in categories:
        categorized[category] = [t for t in templates if t.category and t.category.lower() == category]
        
    return categorized, sorted(list(categories))

def get_company_details():
    """Fetches the single row of company contact and detail information."""
    with current_app.app_context():        
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
    with current_app.app_context():       
        try:
            images = Image.query.order_by(Image.order_index).all()
            image_dict = {
                'vision': [],
                'logo': [],
                'services': {},
                'solutions': {}
            }
            for img in images:
                if img.section == 'vision' or img.section == 'logo':
                    image_dict[img.section].append({
                        'image_url': img.image_url,
                        'alt_text': img.alt_text
                    })
                elif img.section == 'services' and img.service_name:
                    if img.service_name not in image_dict['services']:
                        image_dict['services'][img.service_name] = []
                    image_dict['services'][img.service_name].append({
                        'image_url': img.image_url,
                        'alt_text': img.alt_text
                    })
                elif img.section == 'solutions' and img.service_name:
                    if img.service_name not in image_dict['solutions']:
                        image_dict['solutions'][img.service_name] = []
                    image_dict['solutions'][img.service_name].append({
                        'image_url': img.image_url,
                        'alt_text': img.alt_text
                    })
            
            if not images:                
                result = db.session.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'images')")
                table_exists = result.scalar()                
            return image_dict
        except SQLAlchemyError as e:            
            return {}
        except Exception as e:            
            return {}

def format_templates_for_json(templates):
    """Formats a list of Template objects into a list of dicts for rendering."""
    with current_app.app_context():
        return [
            {"id": t.id, 
             "name": t.name, 
             "description": t.description, 
             "preview": url_for('static', filename='templates/preview_' + t.name.lower().replace(' ', '_') + '.jpg')
            } for t in templates
        ]