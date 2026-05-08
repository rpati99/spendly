# Testing

## Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
python3 -m pip install -r requirements.txt   # use python3 -m pip on macOS if pip not on PATH

# Run dev server (port 5001)
python3 app.py

# Run all tests
pytest

# Run a specific test file
pytest tests/test_foo.py

# Run a specific test by name
pytest -k "test_name"

# Run tests with output visible
pytest -s
```

## Subagent policy

- Always use the builtin `explore` subagent for codebase exploration before implementing any new feature
- Always use a subagent to verify test results after any implementation
- When asked to plan, delegate codebase research to a subagent before presenting the plan
- Always use the builtin `plan` subagent in plan mode