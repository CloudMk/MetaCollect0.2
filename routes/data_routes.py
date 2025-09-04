from flask import Blueprint,render_template,redirect,session,send_file,flash,url_for
from functools import wraps
from flask_login import login_required, current_user
from database.models import Form, Submission
from extensions.extensions import db
import io
import csv
from openpyxl import Workbook

data_bp = Blueprint('data', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si l'utilisateur est connecté
        if not session.get('user_id'):  # ou 'username' selon ta session
            flash("Vous devez être connecté pour accéder à cette page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@data_bp.route('/export/<int:form_id>/<format>')
def export_data(form_id, format):
    form = Form.query.get_or_404(form_id)
    if form.project.user_id != current_user.id:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    submissions = Submission.query.filter_by(form_id=form_id).all()
    
    if format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        headers = [field.label for field in form.fields]
        headers.append('Date de soumission')
        writer.writerow(headers)
        
        # Data
        for submission in submissions:
            row = [submission.data.get(field.name, '') for field in form.fields]
            row.append(submission.submitted_at.strftime('%d/%m/%Y %H:%M'))
            writer.writerow(row)
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{form.name}_data.csv'
        )
    
    elif format == 'excel':
        wb = Workbook()
        ws = wb.active
        
        # Headers
        headers = [field.label for field in form.fields]
        headers.append('Date de soumission')
        ws.append(headers)
        
        # Data
        for submission in submissions:
            row = [submission.data.get(field.name, '') for field in form.fields]
            row.append(submission.submitted_at.strftime('%d/%m/%Y %H:%M'))
            ws.append(row)
        
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue()),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'{form.name}_data.xlsx'
        )