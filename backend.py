from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    # No x=0 default. Just render login form cleanly.
    return render_template("home.html")

@app.route("/authorisation", methods=["POST"])
def authorisation():
    un = request.form.get("username", "")
    p = request.form.get("password", "")

    if un == "Co-Owner-One" and p == "Quantum-Space":
        return render_template("coone.html")
    else:
        # Redirect back to home but with query string ?error=1
        return redirect(url_for("home_error"))

@app.route("/error", methods=["GET"])
def home_error():
    return render_template("home.html", error=1)

if __name__ == "__main__":
    app.run(debug=True)
