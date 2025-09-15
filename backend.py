from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    invite_key = db.Column(db.String(50), nullable=False)
    verified = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

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

@app.route("/error", methods=["GET"])
def home_error():
    return render_template("home.html", error=1)

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    invite_key = request.form.get("invite_key", "")

    if invite_key != os.getenv("INVITE_KEY"):
        return "Invalid invite key!", 400

    new_user = User(username=username, email=email, password=password, invite_key=invite_key, verified=False)
    db.session.add(new_user)
    db.session.commit()

    return "Account created! Please verify email before login."

if __name__ == "__main__":
    app.run(debug=True)
