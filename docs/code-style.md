# Code Style

## Python

- PEP 8 throughout
- snake_case for all variables and functions
- Python 3.10+ — f-strings and `match` statements are fine
- Route functions have one responsibility only: fetch data, render template, done
- Use `abort()` for HTTP errors — never `return "error string"`

## SQL

- Always use parameterized queries with `?` placeholders
- Never use f-strings or string concatenation in SQL
- FK enforcement is manual — `get_db()` must run `PRAGMA foreign_keys = ON` on every connection

## Templates

- Every internal link must use `url_for()` — never hardcode URLs
- All templates must extend `base.html`

## JavaScript

- Vanilla JS only — no frameworks, no jQuery, no npm packages