from flask_login import UserMixin
from datetime import datetime
from extensions.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1200), nullable=False)
    profil = db.Column(db.String(200), default="user") 
    projects = db.relationship('Project', backref='owner', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', back_populates='user', cascade="all, delete-orphan")

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    form_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # clé étrangère qui lie au User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # relation avec User
    user = db.relationship('User', back_populates='projects')

class Form(db.Model):
    __tablename__ = "form"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    fields = db.relationship('Field', backref='form', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='form', lazy=True)
    is_shared = db.Column(db.Boolean, default=False)
    share_url = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Field(db.Model):
    __tablename__ = "field"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)
    is_required = db.Column(db.Boolean, default=False)
    options = db.Column(db.JSON)
    order = db.Column(db.Integer, default=0)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)

class Submission(db.Model):
    __tablename__ = "submission"
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
