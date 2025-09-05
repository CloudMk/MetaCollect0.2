from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from database.models import Project, db

project_bp = Blueprint("projects", __name__)

@project_bp.route("/projects/create", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        form_type = request.form.get("form_type")
        user_id = session.get("user_id")

        if not user_id:
            flash("Vous devez être connecté pour créer un projet", "danger")
            return redirect(url_for("auth_bp.login"))

        try:
            new_project = Project(
                name=name,
                description=description,
                start_date=datetime.strptime(start_date, "%Y-%m-%d"),
                end_date=datetime.strptime(end_date, "%Y-%m-%d"),
                form_type=form_type,
                user_id=user_id
            )
            db.session.add(new_project)
            db.session.commit()
            flash("Projet créé avec succès ✅", "success")
            return redirect(url_for("projects.create_project"))

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la création du projet : {str(e)}", "danger")

    # récupérer tous les projets
    projects = Project.query.all()

    return render_template("create_project.html",projects=projects,now=datetime.now())
