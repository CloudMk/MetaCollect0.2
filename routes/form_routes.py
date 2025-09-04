from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify,session
from flask_login import login_required, current_user
from database.models import Project, Form, Field, Submission
from extensions.extensions import db
from datetime import datetime
from functools import wraps
import uuid

form_bp = Blueprint('forms', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si l'utilisateur est connecté
        if not session.get('user_id'):  # ou 'username' selon ta session
            flash("Vous devez être connecté pour accéder à cette page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@form_bp.route('/create/<int:project_id>', methods=['GET', 'POST'])
def create_form(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        form_data = request.json
        form = Form(
            name=form_data['name'],
            description=form_data.get('description', ''),
            project_id=project_id,
            share_url=str(uuid.uuid4())[:8]
        )
        db.session.add(form)
        db.session.flush()
        
        for i, field_data in enumerate(form_data['fields']):
            field = Field(
                name=field_data['name'],
                label=field_data['label'],
                field_type=field_data['type'],
                is_required=field_data.get('required', False),
                options=field_data.get('options'),
                order=i,
                form_id=form.id
            )
            db.session.add(field)
        
        db.session.commit()
        return jsonify({'success': True, 'form_id': form.id})
    
    return render_template('create_form.html', project=project)

@form_bp.route('/<int:form_id>/view')
def view_form(form_id):
    form = Form.query.get_or_404(form_id)
    if not form.is_shared and (not current_user.is_authenticated or form.project.user_id != current_user.id):
        flash('Formulaire non accessible', 'error')
        return redirect(url_for('auth.login'))
    return render_template('form_view.html', form=form)

@form_bp.route('/<int:form_id>/submit', methods=['POST'])
def submit_form(form_id):
    form = Form.query.get_or_404(form_id)
    data = request.json
    
    submission = Submission(
        form_id=form_id,
        data=data
    )
    db.session.add(submission)
    db.session.commit()
    
    return jsonify({'success': True})

@form_bp.route('/<int:form_id>/share', methods=['POST'])
def toggle_share(form_id):
    form = Form.query.get_or_404(form_id)
    if form.project.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403
    
    data = request.json
    form.is_shared = data.get('shared', False)
    db.session.commit()
    
    return jsonify({'success': True})