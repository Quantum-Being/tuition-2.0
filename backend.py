from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "temporary-secret")  # optional fallback


# -------------------------------------------------------------------
# GOOGLE SHEETS HELPERS
# -------------------------------------------------------------------
def get_all_users():
    try:
        gc = gspread.service_account(filename="service_account.json")
        sheet = gc.open_by_key("1hSeoPx-AK8hVmvAO7SgiSTa602iwfayhFt2eEtJVySc").sheet1
        return sheet.get_all_records()
    except Exception as e:
        print("Error reading Google Sheets:", e)
        return []


def add_user(user_data):
    try:
        gc = gspread.service_account(filename="service_account.json")
        sheet = gc.open_by_key("1hSeoPx-AK8hVmvAO7SgiSTa602iwfayhFt2eEtJVySc").sheet1
        sheet.append_row([user_data["username"], user_data["password"]])
        return True
    except Exception as e:
        print("Error adding user:", e)
        return False


# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        un = request.form.get("username", "")
        p = request.form.get("password", "")

        # Co-owners (admins)
        if un == os.getenv("AAYUSH") and p == os.getenv("COOWNER_1"):
            return render_template("coone.html", google_sheet_api_url=os.getenv("GOOGLE_SHEET_API_URL"))
        elif un == os.getenv("NISHA") and p == os.getenv("COOWNER_2"):
            return render_template("cotwo.html", google_sheet_api_url=os.getenv("GOOGLE_SHEET_API_URL"))

        # Regular user validation
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
    username = request.form.get("username")
    password = request.form.get("password")
    invite_key = request.form.get("invite_key")

    if invite_key != os.getenv("INVITE_KEY"):
        flash("Invalid invite key!")
        return redirect(url_for("home"))

    users = get_all_users()

    if any(u.get("username") == username for u in users):
        flash("Username already exists! Please choose another one.")
        return redirect(url_for("home"))
    else:
        add_user({"username": username, "password": password})
        flash("Account created successfully! Please sign in.")
        return redirect(url_for("home"))


@app.route("/ivgstd", methods=["POST"])
def investigation():
    username = request.form.get("username", "").strip()
    student_id = request.form.get("student_id", "").strip()
    users = get_all_users()

    student = next(
        (u for u in users if u.get("username") == username or str(u.get("student_id")) == student_id),
        None
    )

    return render_template("isd.html", student=student, searched=True)


# -------------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=False)
