# Spec: Edit Expense

## Overview
The Edit Expense feature allows logged-in users to modify an existing expense they own. The user can change the amount, category, date, and description. This is Step 8 in the Spendly roadmap and builds on the Add Expense feature (Step 7) and user authentication (Step 3).

## Depends on
- Step 3 (Registration/Login/Logout) — Requires user authentication via session
- Step 7 (Add Expense) — Requires existing expenses to edit; reuses `create_expense` DB function pattern

## Routes
- `GET /expenses/<int:id>/edit` — Render the edit expense form pre-populated with existing data — logged-in only
- `POST /expenses/<int:id>/edit` — Validate and update the expense, redirect to dashboard — logged-in only

## Database changes
No new tables or columns. The `expenses` table already has all required fields.

New functions needed in `database/db.py`:
- `get_expense_by_id(id)` — retrieves a single expense row by id
- `update_expense(id, user_id, amount, category, date, description)` — updates an expense row

## Templates
- **Create:** `templates/edit_expense.html` — edit form identical in layout to `add_expense.html` but pre-populated and with Save Changes button
- **Modify:** `templates/dashboard.html` — add an edit icon/link to each expense row

## Files to change
- `app.py` — replace the stub `edit_expense` route with full implementation
- `database/db.py` — add `get_expense_by_id()` and `update_expense()` functions
- `templates/dashboard.html` — add edit action per expense row

## Files to create
- `templates/edit_expense.html`

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs — use parameterized SQLite queries only
- Passwords hashed with werkzeug (already done, not new here)
- Use CSS variables from style.css — never hardcode hex values
- All templates extend `base.html`
- Capitalize category on update (same mapping as Step 7: `food` → `Food`, `travel` → `Transport`, etc.)
- Verify expense ownership before rendering or updating — return 404 if not found or not owned

## Definition of done
- [ ] GET `/expenses/<id>/edit` returns 404 when expense does not exist
- [ ] GET `/expenses/<id>/edit` returns 404 when expense belongs to another user
- [ ] GET `/expenses/<id>/edit` renders form pre-populated with existing amount, category, date, description
- [ ] GET `/expenses/<id>/edit` redirects to login with error flash when not logged in
- [ ] POST `/expenses/<id>/edit` updates expense in database and redirects to dashboard with success flash
- [ ] POST `/expenses/<id>/edit` shows error flash when required fields (amount, category, date) are missing
- [ ] POST `/expenses/<id>/edit` preserves category capitalization on update
- [ ] POST `/expenses/<id>/edit` returns 404 when updating another user's expense
- [ ] Dashboard shows an edit action (icon or link) for each expense row
- [ ] Flash messages work correctly for success and error cases