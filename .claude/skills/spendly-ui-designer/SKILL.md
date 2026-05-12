---
name: spendly-ui-designer
description: |
  Frontend UI Designer for Spendly (a personal expense tracker). Generates modern,
  production-ready UI components and pages for Spendly. Automatically triggers when
  the user asks to design, create UI, build component, or redesign any page for
  Spendly, such as "Design the dashboard page", "Create UI for the expense form",
  "Build component for category selector", or "Redesign/improve the login page".
  Also triggers on generic UI requests for Spendly even without explicit trigger
  phrases since the user works primarily on this project.
---

# Frontend UI Designer for Spendly

## What This Skill Does

Generates modern, production-ready UI components and pages for the Spendly expense tracker. Always prioritizes:
- Clean, maintainable CSS
- Modular, reusable components
- Consistency with existing design
- Meaningful icons (Lucide/Heroicons)
- Usability and clarity

## Design System Reference

**Always read these files before starting any UI work:**
- `templates/base.html` — layout structure, nav, footer, flash messages
- `static/css/style.css` — CSS variables, existing components, spacing system

The design system uses:
- **Colors**: CSS variables (`--ink`, `--paper`, `--accent`, etc.) from style.css
- **Spacing**: 8px grid system
- **Typography**: DM Sans (body), DM Serif Display (headings)
- **Style**: Minimal fintech-style UI, rounded corners, soft shadows

## UX Decisions (Always Follow)

### Code Quality
- Clean, minimal CSS — avoid boilerplate
- Modular components with clear class names
- Never hardcode hex colors — use CSS variables

### Design Quality
- Modern SaaS look with card-based layouts
- Good spacing and visual hierarchy
- Subtle colors and soft shadows
- Consistent with existing Spendly design

### Icons
- Use Lucide or Heroicons via CDN where relevant
- Match the minimal, clean fintech aesthetic

### Design Rules
- Minimal, clean fintech-style UI
- Rounded corners (`border-radius`)
- Soft shadows
- Consistent spacing (8px grid)
- Avoid clutter or random styles
- Never use generic, dated UI

### Consistency
- Always match existing project design
- If design direction is unclear, ask for reference screenshots

### What to Avoid
- Generic or dated UI components
- Unstructured code dumps
- Hardcoded colors instead of CSS variables
- Copying styles from other frameworks blindly

## Inputs

When the user requests UI work, extract:
1. **Page/component name** (required) — e.g., "expense list", "category selector"
2. **Optional constraints** — specific requirements mentioned
3. **Data context** — what data will the UI display?

## Output

For every UI task:
1. **UI structure** (brief) — HTML structure overview
2. **Layout + key sections** — how the page/component is organized
3. **Important UX decisions** — why certain design choices were made

## Workflow

### Step 1: Understand the Request
- Identify the page or component to build
- Note any specific requirements from the user
- Determine what data/context is needed

### Step 2: Read Design Reference
Before writing any code, read:
- `templates/base.html`
- `static/css/style.css`
- Any relevant existing page for reference (e.g., `templates/dashboard.html`, `templates/login.html`)

### Step 3: Design the UI
Follow the UX decisions above. Create or modify:
- Template files (`.html`) — extend `base.html`
- CSS additions to `static/css/style.css` using existing CSS variables

### Step 4: Implement
- Create files directly in the workspace
- Use `{% block %}` directives in templates
- Keep CSS in `style.css` — no inline styles
- Add new CSS classes following existing naming patterns

## Important Notes

- All templates MUST extend `base.html`
- Use `url_for()` for all internal links — never hardcode URLs
- Forms should use proper `method="POST"` and CSRF considerations
- Flash messages follow existing patterns in `base.html`
- Mobile responsiveness via existing media queries in style.css