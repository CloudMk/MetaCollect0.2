from flask import Blueprint, render_template, request, redirect, flash, url_for
from extensions.extensions import db  # si vous utilisez une DB pour stocker les messages

contact2_bp = Blueprint('contacts', __name__)

# Route GET pour afficher le formulaire
@contact2_bp.route('/contacts', methods=['GET'])
def contacts():
    return render_template('contact2.html')

# Route POST pour traiter le formulaire
@contact2_bp.route('/contacts', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash("Tous les champs sont obligatoires.", "danger")
        return redirect(url_for('contacts.contacts'))

    # Exemple : sauvegarder dans la base de données
    # db.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    # db.commit()

    flash("Votre message a été envoyé avec succès !", "success")
    return redirect(url_for('contacts.contacts'))
