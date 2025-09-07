from app import app, db
from models import init_models

with app.app_context():
    db, Template, ContactSubmission = init_models(app)
    templates = [
        Template(name='Basic Website', description='A sleek corporate site template.', path='/static/templates/basic.html', category='website'),
        Template(name='E-Shop Template', description='A robust e-commerce solution.', path='/static/templates/eshop.html', category='ecommerce')
    ]
    db.session.bulk_save_objects(templates)
    db.session.commit()

print("Database populated successfully!")