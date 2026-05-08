import sqlite3
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "expense_tracker.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    db.commit()


def get_user_by_email(email):
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cur.fetchone()


def get_user_by_id(user_id):
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cur.fetchone()


def get_user_expenses(user_id, limit=20, offset=0):
    db = get_db()
    cur = db.execute(
        "SELECT id, amount, category, date, description, created_at "
        "FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ? OFFSET ?",
        (user_id, limit, offset),
    )
    return cur.fetchall()


def count_user_expenses(user_id):
    db = get_db()
    cur = db.execute("SELECT COUNT(*) as count FROM expenses WHERE user_id = ?", (user_id,))
    return cur.fetchone()["count"]


def get_expense_stats(user_id):
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) as tx_count, COALESCE(SUM(amount), 0) as total_spent, "
        "COALESCE(AVG(amount), 0) as avg_amount FROM expenses WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    total = row["total_spent"]
    tx_count = row["tx_count"]

    cur = db.execute(
        "SELECT MIN(date) as first_date FROM expenses WHERE user_id = ?", (user_id,)
    )
    first_row = cur.fetchone()

    monthly_avg = 0
    if tx_count > 0 and first_row["first_date"]:
        import datetime
        from datetime import datetime as dt
        first = dt.strptime(first_row["first_date"], "%Y-%m-%d")
        now = dt.now()
        months = max((now.year - first.year) * 12 + (now.month - first.month), 1)
        monthly_avg = round(total / months, 2)

    return {
        "total_spent": round(total, 2),
        "tx_count": tx_count,
        "avg_amount": round(row["avg_amount"], 2),
        "monthly_avg": monthly_avg,
    }


def get_category_breakdown(user_id):
    db = get_db()
    cur = db.execute(
        "SELECT category, COUNT(*) as tx_count, COALESCE(SUM(amount), 0) as total "
        "FROM expenses WHERE user_id = ? GROUP BY category ORDER BY total DESC",
        (user_id,),
    )
    rows = cur.fetchall()

    grand_total = sum(r["total"] for r in rows) or 1
    breakdown = []
    for r in rows:
        breakdown.append({
            "category": r["category"],
            "total": round(r["total"], 2),
            "tx_count": r["tx_count"],
            "pct": round(r["total"] / grand_total * 100, 1),
        })
    return breakdown


def seed_db():
    db = get_db()
    cur = db.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] > 0:
        return

    pw_hash = generate_password_hash("demo123", method="pbkdf2:sha256")
    db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", pw_hash),
    )

    expenses = [
        ("Food", 12.50, "2026-05-02", "Grocery run"),
        ("Food", 8.00, "2026-05-05", "Coffee and pastry"),
        ("Transport", 25.00, "2026-05-03", "Uber to airport"),
        ("Bills", 120.00, "2026-05-01", "Electricity bill"),
        ("Health", 45.00, "2026-05-04", "Pharmacy"),
        ("Entertainment", 15.99, "2026-05-06", "Netflix subscription"),
        ("Shopping", 89.99, "2026-05-07", "New headphones"),
        ("Other", 10.00, "2026-05-08", "Miscellaneous"),
    ]
    for cat, amt, dt, desc in expenses:
        db.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (1, amt, cat, dt, desc),
        )
    db.commit()
