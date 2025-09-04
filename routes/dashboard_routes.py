from flask import Blueprint, render_template,redirect,session,flash,url_for
from functools import wraps
from flask_login import login_required
from extensions.extensions import db


dashboard_bp = Blueprint("dashboard", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si l'utilisateur est connecté
        if not session.get('user_id'):  # ou 'username' selon ta session
            flash("Vous devez être connecté pour accéder à cette page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route("/dashboard",  endpoint='dashboard')
def dashboard():

    return render_template("dashboard.html")


