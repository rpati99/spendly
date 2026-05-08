import sqlite3
from flask import g
from werkzeug.security import generate_password_hash

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
