# simple-flask-service

*Read this in other languages: [English](README.md)*

Простой REST API для управления задачами. Служит демонстрационным приложением
для тестирования библиотеки
[flask-service-metrics](https://github.com/damakalshchikov/flask-service-metrics).

**Стек:** Python 3.14, Flask 3, flask-smorest (REST + OpenAPI), Flask-SQLAlchemy,
PostgreSQL 17, gunicorn, Docker.

## Запуск в Docker

```bash
docker compose up --build
```

API доступен на `http://localhost:5001`. Схема базы применяется автоматически
из `schema.sql` при первом старте контейнера `db`.

## Локальный запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
# Нужен запущенный PostgreSQL; DSN по умолчанию:
# postgresql+psycopg2://postgres:postgres@localhost:5432/simple-database
# (переопределяется переменной окружения DATABASE_URL)
python run.py   # dev-сервер на порту 5000
```

## API

Интерактивная документация (Swagger UI): `http://localhost:5001/api/docs/swagger-ui`.

| Метод | Путь | Описание |
|---|---|---|
| GET, POST | `/projects/` | Список / создание проектов |
| GET, PATCH, DELETE | `/projects/<uuid>` | Один проект |
| GET, POST | `/tasks/` | Список (фильтры: `project_id`, `status`) / создание задач |
| GET, PATCH, DELETE | `/tasks/<uuid>` | Одна задача |
| GET, POST | `/tasks/<uuid>/comments` | Комментарии задачи |
| DELETE | `/task_comments/<uuid>` | Удаление комментария |
| GET | `/health`, `/health/db` | Живость / соединение с БД |

Пример:

```bash
curl -X POST http://localhost:5001/projects/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "Мой проект", "description": "Необязательно"}'
```

## Модель данных

`Project` → `Task` → `TaskComment` с каскадным удалением. У задачи есть
`status` (`todo` / `in_progress` / `done`), `priority` (`low` / `medium` /
`high`), необязательные `assignee` и `due_date`.
