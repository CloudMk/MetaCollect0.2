import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv
from models import db
from extensions.extensions import db, login_manager, migrate
from routes.all_routes import register_routes
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse

load_dotenv()

app = Flask("create_app",__name__)

def create_app():
    app = Flask(__name__)

    # ----------------------
    # Configurations
    # ----------------------
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-secret-key-change-in-production'
    )
    database_url = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:Faly@localhost/metacollection'
    )

    # Création automatique de la base si elle n'existe pas (uniquement localhost)
    if 'localhost' in database_url:
        create_database_if_not_exists(database_url)

    # SQLAlchemy config
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisation extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # LoginManager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."

    # Routes
    register_routes(app)

    @app.route('/')
    def welcome():
        return redirect(url_for('welcome.welcome'))

    @app.route('/auth')
    def index():
        return redirect(url_for('auth.login'))

    # Création des tables
    with app.app_context():
        db.create_all()

    return app


def create_database_if_not_exists(database_url):
    """Créer automatiquement la base PostgreSQL si elle n'existe pas."""
    try:
        result = urlparse(database_url)
        database_name = result.path[1:]  

        conn = psycopg2.connect(
            host=result.hostname,
            user=result.username,
            password=result.password,
            port=result.port or 5432,
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (database_name,))
        if not cursor.fetchone():
            cursor.execute(f'CREATE DATABASE "{database_name}"')
            print(f"Base de données '{database_name}' créée avec succès !")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Erreur lors de la création de la base: {e}")

def init_db():
    """Initialiser la base de données avec les tables"""
    from models import db
    with app.app_context():
        db.create_all()
        print("Tables créées avec succès!")