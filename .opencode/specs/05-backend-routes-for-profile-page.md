# Spec: Backend Routes for Profile Page

## Overview
Add backend routes that complete the profile page feature. Step 04 built the core profile route (name update + password change). This step adds account deletion with password confirmation, giving users full control over their account lifecycle.

## Depends on
- Profile (Step 04) — the profile template and basic GET/POST routes must exist

## Routes
- `POST /profile/delete` — delete the authenticated user's account after password confirmation — logged-in only

## Database changes
- Add `delete_user(user_id)` helper to `database/db.py`

## Templates
- **Modify:** `templates/profile.html` — add a "Delete Account" card with password confirmation form and warning text

## Files to change
- `app.py` — implement `POST /profile/delete` route
- `database/db.py` — add `delete_user(user_id)` function
- `templates/profile.html` — add delete account form section
- `static/css/style.css` — add styles for delete account card (danger styling)

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use sqlite3 directly with `get_db()`
- Parameterised queries only (`?` placeholders) — no f-string interpolation in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use Flask `session` for authentication — store `user_id` in session
- Use `flash()` for error/success messages — render in templates
- All templates extend `base.html`
- Use CSS variables — never hardcode hex color values
- Require password confirmation before deleting account
- Clear session and delete all user expenses before deleting the user
- Use `abort()` for HTTP errors, never raw string returns

## Definition of done
- [ ] `POST /profile/delete` with wrong password shows flash error and does not delete
- [ ] `POST /profile/delete` with correct password deletes the user, clears session, and redirects to landing
- [ ] All expenses belonging to the deleted user are also deleted (cascading delete)
- [ ] "Delete Account" card appears on the profile page with password field and warning
- [ ] Unauthenticated users are redirected to login when accessing `/profile/delete`
- [ ] All queries use parameterised `?` placeholders
- [ ] `delete_user(user_id)` helper exists in `database/db.py`
