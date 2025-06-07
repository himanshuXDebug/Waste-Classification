from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db_connection():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'ECOFY.db'), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user:
            if user["password"] == password:
                session["user_id"] = user["id"]
                session["email"] = user["email"]
                flash("Logged in successfully!", "success")
                return redirect(url_for("profile"))
            else:
                flash("Incorrect password!", "danger")
        else:
            flash("User does not exist!", "danger")

    return render_template("Login.html")

@auth_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        try:
            # Check if the email already exists
            existing_user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if existing_user:
                flash("Email already exists!", "danger")
                return redirect(url_for("auth.signup"))

            # Insert the new user
            conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        finally:
            conn.close()

    return render_template("Signup.html")


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for("auth.login"))
