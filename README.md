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

`Project` -> `Task` -> `TaskComment` with cascade deletion. A task has a
`status` (`todo` / `in_progress` / `done`), a `priority` (`low` / `medium` /
`high`), an optional `assignee` and a `due_date`.

## Metrics and monitoring

This branch integrates the
[flask-service-metrics](https://github.com/damakalshchikov/flask-service-metrics)
library: the app exposes performance metrics (HTTP, SQL, instrumented
functions, process) and ships with a ready Prometheus + Grafana stack.

### Installing the metrics library

The package is published on TestPyPI; for local development:

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ flask-service-metrics
```

The Docker image installs it from a local wheel instead
(`wheels/flask_service_metrics-0.1.1-py3-none-any.whl`, referenced in
`requirements.txt`), so the build does not depend on an external index.
After changing the library, rebuild the wheel (`python -m build` in its
repository), copy it into `wheels/` and update the file name in
`requirements.txt`.

### How it is wired into the app

- `app/extensions.py` - `metrics = FlaskMetrics()`; initialized in the app
  factory via `metrics.init_app(app)`. HTTP metrics need nothing else:
  they are collected by request hooks.
- `app/config.py` - `METRICS_NAMESPACE = "taskservice"`; `/metrics` and the
  health endpoints are excluded from HTTP metrics; `METRICS_LOG_FILE` /
  `METRICS_LOG_INTERVAL` come from environment variables (docker-compose sets
  a JSONL dump to `/tmp/metrics.jsonl` every 30 s).
- `app/resources/common.py` - the `@measure` decorator on `get_or_404` as an
  example of method-level metrics.

### Where to look at the metrics

| What | Where |
|---|---|
| Grafana dashboard | <http://localhost:3000/d/flask-svc-metrics> - no login required |
| Raw Prometheus text format | <http://localhost:5001/metrics> |
| Prometheus UI | <http://localhost:9090> |
| JSONL log dump | `docker compose exec app tail /tmp/metrics.jsonl` |

The dashboard shows HTTP RPS, p95 latency, response codes and exceptions per
endpoint, SQL rate and duration per operation, `@measure`-instrumented
functions, and process metrics (CPU, RSS, threads, GC), refreshing every 5
seconds. Prometheus scrapes the app every 5 seconds.

You can generate load like this:

```bash
for i in $(seq 1 500); do curl -s -o /dev/null http://localhost:5001/projects/; done
```
