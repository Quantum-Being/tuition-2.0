from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import requests

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# SheetDB API URL
SHEET_API_URL = os.getenv("SHEET_API_URL")

# Helper functions
def get_all_users():
    res = requests.get(SHEET_API_URL)
    if res.status_code == 200:
        return res.json()
    return []

def add_user(user_data):
    res = requests.post(SHEET_API_URL, json={"data": [user_data]})
    return res.status_code in [200, 201]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        un = request.form.get("username", "")
        p = request.form.get("password", "")

        # Hardcoded co-owners
        if un == os.getenv("AAYUSH") and p == os.getenv("COOWNER_1"):
            return render_template("coone.html", GOOGLE_SHEET_API_URL=os.getenv("GOOGLE_SHEET_API_URL"))
        elif un == os.getenv("NISHA") and p == os.getenv("COOWNER_2"):
            return render_template("cotwo.html", GOOGLE_SHEET_API_URL=os.getenv("GOOGLE_SHEET_API_URL"))

        # Check users from SheetDB
        users = get_all_users()
        user = next((u for u in users if u["username"] == un and u["password"] == p), None)
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

        users = get_all_users()
        if any(u["username"] == username for u in users):
            flash("Username already exists! Please choose another one.")
            return redirect(url_for("signup"))

        new_user = {"username": username, "password": password}

        if add_user(new_user):
            flash("Account created successfully! You can now sign in.")
            return redirect(url_for("home"))
        else:
            flash("Error adding user. Try again later.")
            return redirect(url_for("signup"))

    return render_template("signup.html")

@app.route("/api/users", methods=["GET"])
def show_users():
    return jsonify(get_all_users())

if __name__ == "__main__":
    app.run(debug=True)
