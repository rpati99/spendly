# Spec: Profile

## Overview
The Profile page allows logged-in users to view and update their account information. Users can change their display name and password, ensuring their account remains secure and personalized.

## Depends on
- Registration (Step 2) — user authentication and session management must be working
- Login and Logout (Step 3) — users must be able to authenticate

## Routes
- `GET /profile` — display profile form with current user data — logged-in only
- `POST /profile` — update name and/or password — logged-in only

## Database changes
No new tables or columns. The `users` table already has all required fields:
- `id`, `name`, `email`, `password_hash`, `created_at`

A `get_user_by_id(id)` function will be needed in `database/db.py`.

## Templates
- **Create:** `templates/profile.html` — profile form with name field, password change fields, and delete account option

## Files to change
- `app.py` — implement `GET /profile` and `POST /profile` routes
- `database/db.py` — add `get_user_by_id(id)` function

## Files to create
- `templates/profile.html` — profile page template

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders)
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Require re-authentication before changing password
- Session must be cleared on password change

## Definition of done
- [ ] `GET /profile` renders profile form with user's current name and email
- [ ] `POST /profile` with valid name updates the user's name in the database
- [ ] `POST /profile` with valid new password updates the password hash
- [ ] Flash messages appear for success and error states
- [ ] Unauthenticated users are redirected to login when accessing `/profile`
- [ ] Profile page shows user registration date