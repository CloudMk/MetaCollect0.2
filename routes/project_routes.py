from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import current_user
from database.models import Project, Form
from extensions.extensions import db
from datetime import datetime
from functools import wraps

project_bp = Blueprint('projects', __name__)

# Liste des projets de l'utilisateur
@project_bp.route('/projects')
def projects():
    user_id = session.get('user_id')
    projects = Project.query.filter_by(user_id=user_id).all() if user_id else []
    return render_template('projects.html', projects=projects)

# Création d'un projet
@project_bp.route('/projects/create', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project = Project(
            name=request.form['name'],
            description=request.form['description'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            form_type=request.form['form_type'],
            user_id=session['user_id']  # ✅ déjà garanti
        )

        db.session.add(project)
        db.session.commit()
        flash('Projet créé avec succès', 'success')
        return redirect(url_for('projects.projects'))

    return render_template('create_project.html')

# Détail d'un projet
@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def project_detail(project_id):
    user_id = session.get('user_id')
    projects = Project.query.get_or_404(project_id)
    if projects.user_id != user_id:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('project_detail.html', projects=projects)

# Vue des données du projet
@project_bp.route('/projects/<int:project_id>/data')
def view_data(project_id):
    user_id = session.get('user_id')
    project = Project.query.get_or_404(project_id)
    if project.user_id != user_id:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    forms = Form.query.filter_by(project_id=project_id).all()
    return render_template('data_view.html', project=project, forms=forms)

# Création d'un formulaire pour un projet
@project_bp.route('/projects/<int:project_id>/create_form', methods=['GET', 'POST'])
def create_form(project_id):
    user_id = session.get('user_id')
    project = Project.query.get_or_404(project_id)
    if project.user_id != user_id:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('projects.projects'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_form = Form(name=name, description=description, project_id=project.id)
        db.session.add(new_form)
        db.session.commit()
        flash('Formulaire créé avec succès', 'success')
        return redirect(url_for('projects.project_detail', project_id=project.id))

    return render_template('create_form.html', project=project)

# API pour partager/départager un formulaire
@project_bp.route('/projects/form/<int:form_id>/share', methods=['POST'])
def share_form(form_id):
    user_id = session.get('user_id')
    form = Form.query.get_or_404(form_id)
    if form.project.user_id != user_id:
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    data = request.get_json()
    form.is_shared = data.get('shared', False)
    db.session.commit()
    return jsonify({'success': True, 'shared': form.is_shared})

# Vue d'un formulaire
@project_bp.route('/form/<int:form_id>/view')
def view_form(form_id):
    user_id = session.get('user_id')
    form = Form.query.get_or_404(form_id)
    if form.project.user_id != user_id:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('projects.projects'))
    return render_template('view_form.html', form=form)

# Export CSV/Excel des données d'un formulaire
@project_bp.route('/form/<int:form_id>/export/<string:format>')
def export_data(form_id, format):
    user_id = session.get('user_id')
    form = Form.query.get_or_404(form_id)
    if form.project.user_id != user_id:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('projects.projects'))
    # Ici tu peux générer le fichier CSV ou Excel selon `format`
    return f"Export {format} pour le formulaire {form.name}"
