from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/CoOwners", methods=["POST"])
def authorisation():
    un = request.form.get("username", "")
    p = request.form.get("password", "")

    if un == os.getenv("AAYUSH") and p == os.getenv("COOWNER_1"):
        return render_template("coone.html")

    elif un == os.getenv("NISHA") and p == os.getenv("COOWNER_2"):
        return render_template("cotwo.html")
        
    else:
        return redirect(url_for("home_error"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        invite_key = request.form.get("invite_key", "")

        if invite_key != os.getenv("INVITE_KEY"):
            flash("Invalid invite key!")
            return redirect(url_for("signup"))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists!")
            return redirect(url_for("signup"))

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.")
        return redirect(url_for("home"))
    
    return render_template("signup.html")

@app.route("/error", methods=["GET"])
def home_error():
    return render_template("home.html", error=1)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
