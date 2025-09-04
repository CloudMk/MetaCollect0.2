from flask import Blueprint, render_template, request, redirect, session, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from urllib.parse import urlparse, urljoin
from database.models import User
from extensions.extensions import db
from email.mime.text import MIMEText
import random
import smtplib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si l'utilisateur est déjà connecté, redirigez-le vers la page d'accueil
    if current_user.is_authenticated:
        return redirect(url_for('accueil.accueil'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        profil = request.form.get('profil')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)  
            session['profil'] = user.profil if user.profil else 'default.png'
            session['username'] = user.username
            flash(f'Bienvenue {user.username} !', 'success')

            # Gestion sécurisée de la redirection avec next
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('accueil.accueil'))

        flash('Identifiants invalides', 'error')

    return render_template('login.html')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        profil = request.form.get('profil')
        password = request.form['password']
        otp_input = request.form.get('otp')

        # Vérifier si le nom d'utilisateur ou email existe
        if User.query.filter_by(username=username).first():
            flash('Nom d\'utilisateur déjà utilisé', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email déjà utilisé', 'error')
            return redirect(url_for('auth.register'))

        # Vérifier OTP stocké en session
        if session.get("confirmation_email") != email or session.get("confirmation_code") != otp_input:
            flash('Code OTP invalide ou non reçu', 'error')
            return redirect(url_for('auth.register'))

        # Créer l'utilisateur
        user = User(
            username=username,
            email=email,
            profil=profil,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        # Supprimer OTP après utilisation
        session.pop("confirmation_code", None)
        session.pop("confirmation_email", None)

        flash('Compte créé avec succès', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"success": False, "message": "Email manquant"}), 400

    # Générer un OTP
    code = str(random.randint(100000, 999999))

    try:
        sender_email = "faliarisoazafindrasojacharlotr@gmail.com"
        app_password = "ocig mghq meao qyqe"  # à sécuriser via .env

        message = MIMEText(f"Votre code de confirmation est : {code}")
        message["Subject"] = "Code de confirmation DataCollect"
        message["From"] = sender_email
        message["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, email, message.as_string())

        # Stocker OTP et email dans session
        session["confirmation_code"] = code
        session["confirmation_email"] = email

        return jsonify({"success": True, "message": "Code envoyé"})
    except Exception as e:
        print("Erreur email:", e)
        return jsonify({"success": False, "message": "Impossible d'envoyer le code"}), 500

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('auth.login'))
