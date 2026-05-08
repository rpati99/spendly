# Spec: Registration

## Overview
Full user registration and login for Spendly. Users can create an account with name, email, and password, then log in to access their personalized expense tracker. Session management keeps users authenticated across pages.

## Depends onx
None — this is the first feature in the Spendly roadmap.

## Routes

| Route | Description | Access |
|---|---|---|
| GET /register | Show registration form | public |
| POST /register | Handle form submission, create user | public |
| GET /login | Show login form | public |
| POST /login | Authenticate user, create session | public |
| GET /logout | Clear session, redirect to login | logged-in |

## Database changes

None — the `users` table already exists in `database/db.py` with all required columns: `id`, `name`, `email`, `password_hash`, `created_at`.

No new tables or columns needed.

## Templates

- **Modify:** `templates/register.html` — add flash message support, form validation feedback
- **Modify:** `templates/login.html` — add flash message support, form validation feedback
- **Modify:** `templates/base.html` — add navbar state for logged-in vs logged-out users

## Files to change

- `app.py` — implement POST handlers for /register and /login, session management
- `templates/register.html` — add error/success feedback
- `templates/login.html` — add error/success feedback
- `templates/base.html` — conditional navbar based on auth state
- `database/db.py` — add `get_user_by_email()` helper

## Files to create

- `templates/dashboard.html` — post-login landing page showing user's expenses

## New dependencies

No new dependencies. Uses werkzeug.security (already installed) for password hashing.

## Rules for implementation

- No SQLAlchemy or ORMs — use sqlite3 directly with `get_db()`
- Parameterised queries only — `?` placeholders, no f-string interpolation in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` using `pbkdf2:sha256`
- Password verification with `werkzeug.security.check_password_hash`
- Use Flask `session` for authentication — store `user_id` in session
- Use `flash()` for error/success messages — render in templates
- All templates extend `base.html`
- Use CSS variables — never hardcode hex color values
- Redirect to `/dashboard` after successful login
- Redirect to `/login` with error if email already exists on registration
- App runs on port 5001 (already configured in app.py)

## Definition of done

- [ ] POST /register creates a new user and redirects to /dashboard
- [ ] POST /register fails gracefully if email already exists (shows error on form)
- [ ] POST /login authenticates valid credentials and redirects to /dashboard
- [ ] POST /login fails gracefully for invalid credentials (shows error on form)
- [ ] GET /logout clears session and redirects to /login
- [ ] Logged-in users see dashboard; logged-out users see login/register
- [ ] Passwords are hashed in the database — not stored in plain text
- [ ] All routes use parameterised queries only