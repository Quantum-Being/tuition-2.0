from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", x=0)

@app.route("/authorisation", methods=["POST"])
def authorisation():
    un = request.form["username"]
    p = request.form["password"]

    if un == "Co-Owner-One" and p == "Quantum-Space":
        return render_template("coone.html")
    else:
        return render_template("home.html", x=1)

if __name__ == "__main__":
    app.run(debug=True)
