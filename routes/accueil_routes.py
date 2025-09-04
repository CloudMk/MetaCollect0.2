from flask import Blueprint, render_template, request, redirect, session
from extensions.extensions import db

accueil_bp = Blueprint('accueil', __name__)

@accueil_bp.route('/accueil')
def accueil():
    return render_template('accueil.html')