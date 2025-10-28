from flask import Flask, render_template, request

app = Flask(__name__)

# Dummy data — replace this with your database function
def get_all_users():
    return [
        {"username": "aayush", "student_id": "101", "age": "13", "grade": "9"},
        {"username": "yk", "student_id": "102", "age": "14", "grade": "9"}
    ]

@app.route("/ivgstd", methods=["GET", "POST"])
def investigation():
    student = None
    searched = False

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        student_id = request.form.get("student_id", "").strip()

        users = get_all_users()
        student = next(
            (u for u in users if u["username"] == username or u["student_id"] == student_id),
            None
        )
        searched = True  # So Jinja knows to show “No match found” if nothing matched

    return render_template("isd.html", student=student, searched=searched)
