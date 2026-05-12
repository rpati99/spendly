from flask import Flask, g, render_template, session, flash, redirect, url_for, request, abort
from datetime import datetime

from database.db import get_db, init_db, seed_db, get_user_by_email, get_user_by_id, get_user_expenses, count_user_expenses, get_expense_stats, get_category_breakdown, create_expense, get_expense_by_id, update_expense
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"


def _parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return None


def _get_date_filters(request_args):
    start = request_args.get("start", type=str)
    end = request_args.get("end", type=str)
    start_date = _parse_date(start)
    end_date = _parse_date(end)
    if start and not start_date:
        flash("Invalid start date format. Use YYYY-MM-DD.", "error")
    if end and not end_date:
        flash("Invalid end date format. Use YYYY-MM-DD.", "error")
    return start_date, end_date


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


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        flash("Please log in to access your profile.", "error")
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    if not user:
        session.clear()
        flash("User not found.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "update_name":
            new_name = request.form.get("name", "").strip()
            if not new_name:
                flash("Name cannot be empty.", "error")
                return redirect(url_for("profile"))

            db = get_db()
            db.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, session["user_id"]))
            db.commit()
            flash("Name updated successfully.", "success")
            return redirect(url_for("profile"))

        elif action == "change_password":
            current_password = request.form.get("current_password", "")
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not current_password or not new_password or not confirm_password:
                flash("All password fields are required.", "error")
                return redirect(url_for("profile"))

            if not check_password_hash(user["password_hash"], current_password):
                flash("Current password is incorrect.", "error")
                return redirect(url_for("profile"))

            if len(new_password) < 8:
                flash("New password must be at least 8 characters.", "error")
                return redirect(url_for("profile"))

            if new_password != confirm_password:
                flash("New passwords do not match.", "error")
                return redirect(url_for("profile"))

            pw_hash = generate_password_hash(new_password, method="pbkdf2:sha256")
            db = get_db()
            db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (pw_hash, session["user_id"]))
            db.commit()

            session.clear()
            flash("Password changed successfully. Please log in again.", "success")
            return redirect(url_for("login"))

    return render_template("profile.html", user=user)


@app.route("/profile/history")
def profile_history():
    if "user_id" not in session:
        flash("Please log in to access your history.", "error")
        return redirect(url_for("login"))

    page = request.args.get("page", 1, type=int)
    per_page = 20
    start_date, end_date = _get_date_filters(request.args)
    expenses = get_user_expenses(session["user_id"], limit=per_page, offset=(page - 1) * per_page, start_date=start_date, end_date=end_date)
    total = count_user_expenses(session["user_id"], start_date=start_date, end_date=end_date)
    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        "profile_history.html",
        expenses=expenses,
        page=page,
        total_pages=total_pages,
        total_count=total,
        start_date=start_date,
        end_date=end_date,
    )


@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if "user_id" not in session:
        flash("Please log in to add an expense.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        amount = request.form.get("amount", type=float)
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()

        if not amount or not category or not date:
            flash("Amount, category, and date are required.", "error")
            return redirect(url_for("add_expense"))

        # Capitalize category (template uses lowercase, seed data uses title case)
        category_map = {
            "food": "Food", "travel": "Transport", "bills": "Bills",
            "shopping": "Shopping", "entertainment": "Entertainment",
            "healthcare": "Health", "other": "Other"
        }
        category = category_map.get(category.lower(), category.title())

        create_expense(session["user_id"], amount, category, date, description)
        flash("Expense added successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_expense.html")


@app.route("/profile/stats")
def profile_stats():
    if "user_id" not in session:
        flash("Please log in to view your stats.", "error")
        return redirect(url_for("login"))

    start_date, end_date = _get_date_filters(request.args)
    stats = get_expense_stats(session["user_id"], start_date=start_date, end_date=end_date)
    return render_template("profile_stats.html", stats=stats, start_date=start_date, end_date=end_date)


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
def edit_expense(id):
    if "user_id" not in session:
        flash("Please log in to edit an expense.", "error")
        return redirect(url_for("login"))

    expense = get_expense_by_id(id)
    if not expense or expense["user_id"] != session["user_id"]:
        abort(404)

    if request.method == "POST":
        amount = request.form.get("amount", type=float)
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()

        if not amount or not category or not date:
            flash("Amount, category, and date are required.", "error")
            return redirect(url_for("edit_expense", id=id))

        category_map = {
            "food": "Food", "travel": "Transport", "bills": "Bills",
            "shopping": "Shopping", "entertainment": "Entertainment",
            "healthcare": "Health", "other": "Other"
        }
        category = category_map.get(category.lower(), category.title())

        update_expense(id, session["user_id"], amount, category, date, description)
        flash("Expense updated successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_expense.html", expense=expense)


@app.route("/profile/categories")
def profile_categories():
    if "user_id" not in session:
        flash("Please log in to view categories.", "error")
        return redirect(url_for("login"))

    start_date, end_date = _get_date_filters(request.args)
    breakdown = get_category_breakdown(session["user_id"], start_date=start_date, end_date=end_date)
    grand_total = sum(b["total"] for b in breakdown)
    return render_template("profile_categories.html", breakdown=breakdown, grand_total=grand_total, start_date=start_date, end_date=end_date)


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


@app.route("/analytics")
def analytics():
    if "user_id" not in session:
        flash("Please log in to access Analytics.", "error")
        return redirect(url_for("login"))

    return render_template("analytics.html")


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
