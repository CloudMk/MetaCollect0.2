from extensions.extensions import db
from .auth_routes import auth_bp
from .project_routes import project_bp
from .form_routes import form_bp
from .data_routes import data_bp
from .dashboard_routes import dashboard_bp
from .welcome_page import welcome_bp
from .update_profile import update_bp
from .accueil_routes import accueil_bp
from .contact_routes import contact_bp
from .contact2_routes import contact2_bp
from .help_routes import help_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(project_bp)
    app.register_blueprint(form_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(welcome_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(accueil_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(contact2_bp)
    app.register_blueprint(help_bp)