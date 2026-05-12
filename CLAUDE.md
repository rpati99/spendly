# Agents

## Setup
```bash
python3 -m venv venv && source venv/bin/activate
python3 -m pip install -r requirements.txt   # use python3 -m pip on macOS if pip not on PATH
```

## Run
```bash
python3 app.py   # http://127.0.0.1:5001
```

## Test
```bash
pytest
pytest -k "test_name"   # specific test
pytest -s                # with output visible
```

## Stack
- Flask 3.1 (debug on port 5001)
- SQLite (db.py is empty stub — `get_db()`, `init_db()`, `seed_db()` to be implemented)
- Vanilla JS + CSS (single `static/css/style.css`)

## Routes
| Route | Status |
|---|---|
| `/` | landing.html |
| `/register` | register.html |
| `/login` | login.html |
| `/terms` | terms.html |
| `/privacy` | privacy.html |
| `/logout` | stub (Step 3) |
| `/profile` | stub (Step 4) |
| `/expenses/add` | stub (Step 7) |
| `/expenses/<id>/edit` | stub (Step 8) |
| `/expenses/<id>/delete` | stub (Step 9) |

**Do not implement a stub route unless the active task explicitly targets that step.**

## Rules
- All routes in `app.py` only — no blueprints
- All DB logic in `database/db.py` — never inline in routes
- Templates extend `base.html`, use `url_for()` for internal links
- Parameterized SQL queries only (`?` placeholders) — no f-string interpolation
- No new pip packages without updating requirements.txt
- Never use raw string returns — always render a template once a route is implemented

## Code style
- Python 3.10+ (f-strings, match statements fine)
- snake_case, PEP 8
- Route functions: one responsibility — fetch data, render template, done
- Use `abort()` for HTTP errors, not `return "error string"`
- Vanilla JS only — no frameworks

## Gotchas
- SQLite FK enforcement off by default; `get_db()` must run `PRAGMA foreign_keys = ON`
- App runs on **port 5001**, not Flask default 5000
- `.gitignore` excludes `expense_tracker.db`, `venv/`, `.env`, `__pycache__/`

## Docs
Additional project docs in `docs/`:
- `docs/architecture.md` — structure and route status
- `docs/testing.md` — test commands
- `docs/constraints.md` — tech stack constraints
- `docs/code-style.md` — Python, SQL, template conventions