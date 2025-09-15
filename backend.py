from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/CoOwners", methods=["POST"])
def authorisation():
    un = request.form.get("username", "")
    p = request.form.get("password", "")

    if un == "Co-Owner-One" and p == os.getenv("COOWNER_ONE_USER"):
        return render_template("coone.html")

    elif un == "Co-Owner-Two" and p == "AayushAayra":
        return render_template("cotwo.html")
        
    else:
        return redirect(url_for("home_error"))

@app.route("/error", methods=["GET"])
def home_error():
    return render_template("home.html", error=1)

if __name__ == "__main__":
    app.run(debug=True)
