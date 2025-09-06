from flask import Blueprint, render_template,redirect,session,flash,url_for
from functools import wraps
from flask_login import login_required
from extensions.extensions import db


dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard",  endpoint='dashboard')
def dashboard():

    return render_template("dashboard.html")


