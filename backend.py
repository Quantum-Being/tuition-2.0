from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    invite_key = db.Column(db.String(150), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        un = request.form.get("username", "")
        p = request.form.get("password", "")

        # Hardcoded co-owners
        if un == os.getenv("AAYUSH") and p == os.getenv("COOWNER_1"):
            return render_template("coone.html")
        elif un == os.getenv("NISHA") and p == os.getenv("COOWNER_2"):
            return render_template("cotwo.html")

        # Check database users
        user = User.query.filter_by(username=un, password=p, email_verified=True).first()
        if user:
            return render_template("user_dashboard.html", username=un)
        else:
            flash("Either username or password is incorrect! Please try again.")
            return redirect(url_for("home"))

    return render_template("signin.html")

@app.route("/onboarding", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        invite_key = request.form.get("invite_key")

        if invite_key != os.getenv("INVITE_KEY"):
            flash("Invalid invite key!")
            return redirect(url_for("signup"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("signup"))

        new_user = User(username=username, password=password, invite_key=invite_key, email_verified=True)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! You can now sign in.")
        return redirect(url_for("home"))

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
