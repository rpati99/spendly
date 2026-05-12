# Spec: Login and Logout

## Overview
Implement user login and logout for Spendly. Users can sign in with their email and password to create an authenticated session, and log out to end it. This step adds session management to the app, enables the `/logout` route, and makes the navbar aware of authentication state.

## Depends on
Step 01 — Database setup (tables, `get_db()`, `seed_db()`)

## Routes
- `POST /login` — authenticate user, create session — public
- `GET /logout` — clear session, redirect to login — logged-in

## Database changes
- Add `get_user_by_email(email)` helper to `database/db.py` — returns a Row or None
- No new tables or columns needed

## Templates
- **Modify:** `templates/base.html` — add flash message container, conditional logged-in/logged-out navbar
- **Modify:** `templates/login.html` — switch to `url_for()` action, use flash messages for errors
- **Create:** `templates/dashboard.html` — post-login landing page with user info and placeholder for expenses

## Files to change
- `app.py` — add `secret_key`, session imports, `POST /login` handler, `GET /logout` handler, `GET /dashboard` route
- `database/db.py` — add `get_user_by_email(email)` helper
- `templates/base.html` — flash message container, conditional navbar
- `templates/login.html` — flash-based error feedback, `url_for('login')` action
- `static/css/style.css` — flash message styles, dashboard layout, logout button in navbar

## Files to create
- `templates/dashboard.html` — simple post-login dashboard with user name and expense placeholder

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use sqlite3 directly with `get_db()`
- Parameterised queries only — `?` placeholders, no f-string interpolation in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use Flask `session` for authentication — store `user_id` in session
- Use `flash()` for error/success messages — render in templates
- All templates extend `base.html`
- Use CSS variables — never hardcode hex color values
- Redirect to `/dashboard` after successful login
- Redirect to `/login` with flash error for invalid credentials
- App runs on port 5001 (already configured in app.py)

## Definition of done
- [ ] POST /login authenticates valid credentials and redirects to /dashboard
- [ ] POST /login shows flash error for invalid email or password
- [ ] GET /logout clears session and redirects to /login
- [ ] Unauthenticated GET /dashboard redirects to /login
- [ ] Navbar shows Dashboard/Profile/Logout when logged in, Sign in/Get started when logged out
- [ ] Flash messages display on login page for errors
- [ ] All queries use parameterised `?` placeholders
- [ ] `get_user_by_email()` helper exists in `database/db.py`
