from flask import Flask, render_template, request, redirect, url_for, flash
import requests, os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")

SHEETDB_URL = os.getenv("SHEET_API_URL", "https://sheetdb.io/api/v1/fa2lss1f8h2sd")

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def get_all_users():
    try:
        res = requests.get(SHEETDB_URL)
        if res.status_code == 200:
            return res.json()
        else:
            print("Error fetching users:", res.status_code)
            return []
    except Exception as e:
        print("Error fetching users:", e)
        return []


def add_user(username, password):
    try:
        data = {"data": [{"username": username, "password": password}]}
        res = requests.post(SHEETDB_URL, json=data)
        return res.status_code in (200, 201)
    except Exception as e:
        print("Error adding user:", e)
        return False

# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        un = request.form.get("username", "").strip()
        p = request.form.get("password", "").strip()

        # Co-owners (admins)
        if un == os.getenv("AAYUSH") and p == os.getenv("COOWNER_1"):
            return render_template("ownr.html", google_sheet_api_url=os.getenv("GOOGLE_SHEET_API_URL"), JHA="Mrs. Aayush Jha")
        elif un == os.getenv("NISHA") and p == os.getenv("COOWNER_2"):
            return render_template("ownr.html", google_sheet_api_url=os.getenv("GOOGLE_SHEET_API_URL"), JHA="Mr. Nisha Jha")

        # Normal users
        users = get_all_users()
        user = next((u for u in users if u.get("username") == un and u.get("password") == p), None)
        if user:
            return render_template("user_dashboard.html", username=un)
        else:
            flash("Either username or password is incorrect! Please try again.")
            return redirect(url_for("home"))

    return render_template("signin.html")


@app.route("/onboarding", methods=["POST"])
def signup():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    invite_key = request.form.get("invite_key", "").strip()

    if invite_key != os.getenv("INVITE_KEY"):
        flash("Invalid invite key!")
        return redirect(url_for("home"))

    users = get_all_users()
    if any(u.get("username") == username for u in users):
        flash("Username already exists!")
        return redirect(url_for("home"))

    if add_user(username, password):
        flash("Account created successfully! Please log in.")
        return redirect(url_for("home"))
    else:
        flash("Error adding user. Try again later.")
        return redirect(url_for("home"))


@app.route("/ivgstd", methods=["GET", "POST"])
def ivgstd():
    student = None
    searched = False

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        student_id = request.form.get("student_id", "").strip()

        try:
            res = requests.get(SHEETDB_URL)
            if res.status_code == 200:
                data = res.json()
                for u in data:
                    if u.get("username") == username or u.get("student_id") == student_id:
                        student = u
                        break
                searched = True
        except Exception as e:
            print("Error accessing account database:", e)

    return render_template("isd.html", student=student, searched=searched)


# -------------------------------------------------------------------
# Run app
# -------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
