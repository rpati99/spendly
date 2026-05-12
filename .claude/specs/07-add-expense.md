# Spec: Add Expense

## Overview
The Add Expense feature allows logged-in users to record new expenses with an amount, category, date, and optional description. This is Step 7 in the Spendly roadmap and builds on the registration (Step 3) and profile (Step 6) infrastructure already in place.

## Depends on
- Step 3 (Registration/Login/Logout) — Requires user authentication via session
- No other steps required

## Routes
- `GET /expenses/add` — Render the add expense form — logged-in only
- `POST /expenses/add` — Validate and insert the expense, redirect to dashboard — logged-in only

## Database changes
No new tables or columns. The `expenses` table from Step 6 already has all required fields.

New function needed in `database/db.py`:
- `create_expense(user_id, amount, category, date, description)` — inserts a new expense row

## Templates
- **Create:** No new templates — `templates/add_expense.html` already exists
- **Modify:** No template modifications

Note: The existing `add_expense.html` uses lowercase category values (`food`, `travel`, etc.) but the seed data uses title case (`Food`, `Transport`, etc.). The implementation must capitalize the category on insert to match existing data.

## Files to change
- `app.py` — implement the `add_expense` route (currently stub)
- `database/db.py` — add `add_expense()` function

## Files to create
None.

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs — use parameterized SQLite queries only
- Categories must be capitalized on insert (Food, Transport, Bills, Health, Entertainment, Shopping, Other)
- Use CSS variables from style.css — never hardcode hex values
- All templates extend `base.html`
- Passwords hashed with werkzeug (already done, not new here)

## Definition of done
- [ ] GET `/expenses/add` renders the form when logged in
- [ ] GET `/expenses/add` redirects to login with error flash when not logged in
- [ ] POST `/expenses/add` inserts expense into database and redirects to dashboard with success flash
- [ ] POST `/expenses/add` validates required fields (amount, category, date) — shows error flash on failure
- [ ] Category is stored with correct capitalization (title case)
- [ ] User cannot add expenses for another user
- [ ] Flash messages work correctly for success and error cases
- [ ] Dashboard link works from the form