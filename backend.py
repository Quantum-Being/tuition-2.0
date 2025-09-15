from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    invite_key = db.Column(db.String(50), nullable=False)
    verified = db.Column(db.Boolean, default=False)

# Create tables (run once)
with app.app_context():
    db.create_all()
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    invite_key = request.form.get("invite_key", "")

    # Check invite key
    if invite_key != os.getenv("INVITE_KEY"):
        return render_template("signup.html", error="Invalid invite key")

    # Check if user/email already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return render_template("signup.html", error="Username or email already exists")

    # Create new user
    new_user = User(username=username, email=email, password=password, invite_key=invite_key)
    db.session.add(new_user)
    db.session.commit()

    return render_template("signup_success.html", username=username)
