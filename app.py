from flask import Flask, g, render_template, session, flash, redirect, url_for, request

from database.db import get_db, init_db, seed_db, get_user_by_email
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return redirect(url_for("register"))

        existing = get_user_by_email(email)
        if existing:
            flash("An account with this email already exists.", "error")
            return redirect(url_for("register"))

        pw_hash = generate_password_hash(password, method="pbkdf2:sha256")
        db = get_db()
        db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, pw_hash),
        )
        db.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")




# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("login"))

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

        session.clear()
        session["user_id"] = user["id"]
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in to access your dashboard.", "error")
        return redirect(url_for("login"))

    db = get_db()
    user = db.execute("SELECT name FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return render_template("dashboard.html", user=user)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
