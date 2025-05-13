# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
import pandas as pd
import os

main_bp = Blueprint("main", __name__)
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@main_bp.route("/")
def index():
    return """
        <h2>Welcome to the Staffing App</h2>
        <p><a href='/login'>Login</a> or <a href='/register'>Register</a></p>
    """


@main_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename.endswith(".xlsx"):
            flash("Please upload a valid Excel (.xlsx) file.")
            return redirect(request.url)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            df = pd.read_excel(filepath)
            session["uploaded_file"] = filepath  # reference for Dash
            flash("File uploaded successfully.")
            return redirect("/dash")  # we’ll wire this in the next step
        except Exception as e:
            flash(f"Error reading file: {e}")
            return redirect(request.url)

    return render_template("upload.html")
