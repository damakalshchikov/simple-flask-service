# simple-flask-service

*Read this in other languages: [Русский](README.ru.md)*

A simple task-management REST API. Serves as a demo application for testing
the [flask-service-metrics](https://github.com/damakalshchikov/flask-service-metrics)
library.

**Stack:** Python 3.14, Flask 3, flask-smorest (REST + OpenAPI), Flask-SQLAlchemy,
PostgreSQL 17, gunicorn, Docker.

## Running with Docker

```bash
docker compose up --build
```

The API is available at `http://localhost:5001`. The database schema is applied
automatically from `schema.sql` on the first start of the `db` container.

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
# PostgreSQL must be running; the default DSN is
# postgresql+psycopg2://postgres:postgres@localhost:5432/simple-database
# (override with the DATABASE_URL environment variable)
python run.py   # dev server on port 5000
```

## API

Interactive documentation (Swagger UI): `http://localhost:5001/api/docs/swagger-ui`.

| Method | Path | Description |
|---|---|---|
| GET, POST | `/projects/` | List / create projects |
| GET, PATCH, DELETE | `/projects/<uuid>` | Single project |
| GET, POST | `/tasks/` | List (filters: `project_id`, `status`) / create tasks |
| GET, PATCH, DELETE | `/tasks/<uuid>` | Single task |
| GET, POST | `/tasks/<uuid>/comments` | Comments of a task |
| DELETE | `/task_comments/<uuid>` | Delete a comment |
| GET | `/health`, `/health/db` | Liveness / DB connectivity |

Example:

```bash
curl -X POST http://localhost:5001/projects/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "My project", "description": "Optional"}'
```

## Data model

`Project` → `Task` → `TaskComment` with cascade deletion. A task has a
`status` (`todo` / `in_progress` / `done`), a `priority` (`low` / `medium` /
`high`), an optional `assignee` and a `due_date`.
