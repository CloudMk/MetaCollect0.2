from flask import Blueprint, render_template, request, redirect, session
from extensions.extensions import db

help_bp = Blueprint('help', __name__)

@help_bp.route('/help')
def help():
    return render_template('apropos.html')