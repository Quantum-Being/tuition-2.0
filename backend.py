from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/authorisation", methods=["POST"])
def authorisation():
    un = request.form["username"]
    p = request.form["password"]

if __name__ == "__main__":
    app.run(debug=True)
