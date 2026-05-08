# Plan: Database Setup (Step 1)

## Goal

Replace the stub in `database/db.py` with a working SQLite implementation and wire it up in `app.py`. This is the data layer foundation for the entire Spendly app.

---

## Files to Change

1. **`database/db.py`** — implement `get_db()`, `init_db()`, `seed_db()`
2. **`app.py`** — add imports and startup calls

No new files to create. No new pip packages required.

---

## Implementation: `database/db.py`

### `get_db()`

```python
import sqlite3
from flask import g

DATABASE = "expense_tracker.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
    return db
```

- Uses Flask's `g` context for connection reuse per request
- Opens `expense_tracker.db` in project root (matching AGENTS.md convention)
- Enables `row_factory = sqlite3.Row` for dict-like access
- Enables `PRAGMA foreign_keys = ON` on every new connection (AGENTS.md gotcha)
- Properly close connection via `teardown_appcontext`

### `init_db()`

```python
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
```

- `CREATE TABLE IF NOT EXISTS` — safe to call multiple times
- Matches schema exactly from spec (users + expenses tables)
- Foreign key enforcement is per-connection (already set in `get_db()`)

### `seed_db()`

```python
from werkzeug.security import generate_password_hash


def seed_db():
    db = get_db()
    cur = db.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] > 0:
        return

    pw_hash = generate_password_hash("demo123")
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
```

- Early return if users table already has rows — prevents duplicate seeding
- Uses `generate_password_hash` (werkzeug, already in requirements)
- Parameterized queries throughout — no f-string interpolation
- 8 sample expenses across categories: Food (×2), Transport, Bills, Health, Entertainment, Shopping, Other
- All dates in YYYY-MM-DD format in current month (May 2026)

### App teardown

Add a function to close the connection at end of request:

```python
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
```

---

## Implementation: `app.py`

### Changes needed

1. **Add imports** at top of file:
   ```python
   from database.db import get_db, init_db, seed_db
   ```

2. **Add startup call** before the `if __name__ == "__main__":` block:
   ```python
   with app.app_context():
       init_db()
       seed_db()
   ```

3. **Add teardown** (inside `close_connection` as shown above)

**No other changes** to existing routes or templates — they remain as-is.

---

## Testing & Verification

After implementation, verify with:

```bash
source venv/bin/activate
python3 app.py
```

- App starts on port 5001 without errors
- `expense_tracker.db` file is created in project root
- Tables `users` and `expenses` exist with correct schema

Check seeded data:

```bash
sqlite3 expense_tracker.db "SELECT * FROM users;"
sqlite3 expense_tracker.db "SELECT * FROM expenses;"
```

- 1 demo user row
- 8 expense rows linked to user_id = 1
- Running `pytest` passes any existing tests
- Re-running `init_db()` / `seed_db()` does not duplicate data

---

## Definition of Done

- [ ] `get_db()` returns a working connection with row_factory and foreign keys
- [ ] `init_db()` creates both tables safely (idempotent)
- [ ] `seed_db()` inserts demo user + 8 sample expenses exactly once
- [ ] `app.py` calls `init_db()` and `seed_db()` on startup
- [ ] `expense_tracker.db` is created on first run
- [ ] Demo user has password hashed with werkzeug
- [ ] All queries are parameterized — no string formatting
- [ ] Foreign key enforcement works (invalid user_id fails)
- [ ] App starts on port 5001 without errors
- [ ] No duplicate data on repeated runs
