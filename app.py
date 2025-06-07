import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO logs

from flask import Flask, request, render_template, send_from_directory, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
from Main import classify_waste, load_artifacts
from routes import auth_blueprint
import numpy as np
import cv2
import tensorflow as tf

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['PROFILE_IMAGES'] = os.path.join(BASE_DIR, 'profile_images')
app.secret_key = 'supersecretkey'

for folder in [app.config['UPLOAD_FOLDER'], app.config['PROFILE_IMAGES']]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_db_connection():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'ECOFY.db'))
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'ECOFY.db'))
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, profile_image TEXT DEFAULT NULL, rewards INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

initialize_db()

model_loaded = False
def ensure_model_loaded():
    global model_loaded
    if not model_loaded:
        load_artifacts()
        model_loaded = True

app.register_blueprint(auth_blueprint)

@app.route("/")
def home():
    logged_in = 'user_id' in session
    return render_template("home.html", logged_in=logged_in, username=session.get('username'))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if 'user_id' not in session:
        flash("Please log in to upload and classify waste.", "info")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if 'file' not in request.files:
            return render_template("404.html"), 400
        file = request.files['file']
        if file.filename == '':
            flash("No selected file. Please choose a file to upload.", "danger")
            return redirect(url_for("upload"))
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        ensure_model_loaded()
        predicted_label, _, _, _, waste_size = classify_waste(file_path)
        conn = get_db_connection()
        conn.execute("UPDATE users SET rewards = rewards + 1 WHERE id = ?", (session['user_id'],))
        conn.commit()
        user = conn.execute("SELECT rewards FROM users WHERE id = ?", (session['user_id'],)).fetchone()
        conn.close()
        flash("Image uploaded successfully! Your rewards have been updated.", "success")
        return render_template("upload.html", filename=filename, predicted_label=predicted_label, waste_size=waste_size, rewards=user['rewards'])
    return render_template("upload.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'user_id' not in session:
        flash("Please log in to access your profile.", "info")
        return redirect(url_for("auth.login"))
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()
    if request.method == "POST":
        new_username = request.form["username"]
        new_password = request.form["password"]
        profile_image = request.files.get("profile_image")
        if profile_image and profile_image.filename != "":
            filename = f"user_{session['user_id']}_{secure_filename(profile_image.filename)}"
            image_path = os.path.join(app.config['PROFILE_IMAGES'], filename)
            profile_image.save(image_path)
        else:
            filename = user["profile_image"]
        conn = get_db_connection()
        conn.execute("UPDATE users SET username = ?, password = ?, profile_image = ? WHERE id = ?", (new_username, new_password, filename, session["user_id"]))
        conn.commit()
        conn.close()
        session["username"] = new_username
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))
    return render_template("Profile.html", user=user)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/profile_images/<filename>')
def profile_image(filename):
    return send_from_directory(app.config['PROFILE_IMAGES'], filename)

print("Running")
if __name__ == "__main__":
    try:
        from waitress import serve
        print("Server running at: http://127.0.0.1:5000")
        serve(app, host="0.0.0.0", port=5000)
    except ImportError:
        app.run(debug=True)
