# Spec: Date Filter for Profile Page

## Overview
Add date range filtering to the profile page views (history, stats, categories) so users can view expenses within a specific time period. This enables better analysis of spending over custom date ranges.

## Depends on
- Backend Routes for Profile Page (Step 05) — profile history, stats, and categories routes must exist

## Routes
No new routes. All existing routes accept optional date filter query parameters:
- `GET /profile/history?start=YYYY-MM-DD&end=YYYY-MM-DD`
- `GET /profile/stats?start=YYYY-MM-DD&end=YYYY-MM-DD`
- `GET /profile/categories?start=YYYY-MM-DD&end=YYYY-MM-DD`

## Database changes
- Add optional `start_date` and `end_date` parameters to `get_user_expenses(user_id, limit, offset, start_date, end_date)` in `database/db.py`
- Add optional `start_date` and `end_date` parameters to `get_expense_stats(user_id, start_date, end_date)` in `database/db.py`
- Add optional `start_date` and `end_date` parameters to `get_category_breakdown(user_id, start_date, end_date)` in `database/db.py`

## Templates
- **Modify:** `templates/profile_history.html` — add date range picker form with start and end date inputs
- **Modify:** `templates/profile_stats.html` — add date range picker form
- **Modify:** `templates/profile_categories.html` — add date range picker form

## Files to change
- `app.py` — update `/profile/history`, `/profile/stats`, `/profile/categories` routes to accept and pass `start` and `end` query params
- `database/db.py` — update `get_user_expenses`, `get_expense_stats`, `get_category_breakdown` to filter by date range
- `templates/profile_history.html` — add date filter form
- `templates/profile_stats.html` — add date filter form
- `templates/profile_categories.html` — add date filter form
- `static/css/style.css` — add styles for date filter forms

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use sqlite3 directly with `get_db()`
- Parameterised queries only (`?` placeholders) — no f-string interpolation in SQL
- Dates passed as `YYYY-MM-DD` strings
- If start or end date is missing, filter should not be applied for that bound
- If start and end are both provided, only expenses between (inclusive) those dates are shown
- Use Flask `request.args.get()` to get query parameters
- Use CSS variables — never hardcode hex color values
- All templates extend `base.html`
- The date filter form should use GET method and preserve other query params on submit

## Definition of done
- [ ] `/profile/history?start=2026-05-01&end=2026-05-07` shows only expenses in that range
- [ ] `/profile/stats?start=2026-05-01&end=2026-05-07` shows stats calculated only for expenses in that range
- [ ] `/profile/categories?start=2026-05-01&end=2026-05-07` shows breakdown for expenses in that range
- [ ] Date filter form appears on all three profile pages
- [ ] Omitting start/end date shows all expenses (no filter applied)
- [ ] Dates outside valid range are ignored (no errors)
- [ ] All queries use parameterised `?` placeholders
- [ ] `get_user_expenses` accepts `start_date` and `end_date` parameters in `database/db.py`
- [ ] `get_expense_stats` accepts `start_date` and `end_date` parameters in `database/db.py`
- [ ] `get_category_breakdown` accepts `start_date` and `end_date` parameters in `database/db.py`