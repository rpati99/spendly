# Constraints

## Tech stack — do not deviate

- **Flask only** — no FastAPI, no Django, no other web frameworks
- **SQLite only** — no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only** — no React, no jQuery, no npm packages
- **No new pip packages** — work within `requirements.txt` as-is unless explicitly told otherwise

## Hard rules

- Never put DB logic in route functions — it belongs in `database/db.py`
- Never install new packages mid-feature without flagging it — keep `requirements.txt` in sync
- Never use raw string returns for stub routes once a step is implemented — always render a template
- `database/db.py` is currently empty — do not assume helpers exist until the step that implements them
- The app runs on **port 5001**, not the Flask default 5000 — don't change this