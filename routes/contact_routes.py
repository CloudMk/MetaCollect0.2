from flask import Blueprint, render_template, request, redirect, session
from extensions.extensions import db

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact')
def contact():
    return render_template('contact.html')