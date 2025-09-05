from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask_login import login_required, current_user
from extensions.extensions import db
from flask_login import  login_required, current_user
from functools import wraps

update_bp = Blueprint('update_profile', __name__, template_folder='templates')

@update_bp.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        if not username or not email:
            flash("Tous les champs sont obligatoires.", "danger")
            return redirect(url_for('update_profile.update_profile'))

        current_user.username = username
        current_user.email = email

        try:
            db.session.commit()
            flash("Profil mis à jour avec succès.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la mise à jour: {str(e)}", "danger")
        
        return redirect(url_for('update_profile.update_profile'))

    return render_template('profile.html', user=current_user)
