### Hexlet tests and linter status:
[![Actions Status](https://github.com/RustemYeldessov/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/RustemYeldessov/python-project-52/actions)

### Task Manager (Django)

- Deployed app: [Render web service](https://your-render-domain.onrender.com)

### Requirements

- Python 3.10+
- uv (installed automatically in build)

### Local setup

```bash
uv sync --frozen
uv run python manage.py migrate
uv run python manage.py runserver
```

Open `http://127.0.0.1:8000/` to see the greeting.

### Deployment on Render

- Build command: `make build`
- Start command: `make render-start`

Ensure environment variables are set:

- `SECRET_KEY`
- `DEBUG` (optional)
- `ALLOWED_HOSTS` (should include `webserver`)
- `DATABASE_URL` (PostgreSQL)