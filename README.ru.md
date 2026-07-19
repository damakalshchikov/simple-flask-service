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

## Метрики и мониторинг

В этой ветке подключена библиотека
[flask-service-metrics](https://github.com/damakalshchikov/flask-service-metrics):
приложение отдаёт метрики производительности (HTTP, SQL, размеченные функции,
процесс), а рядом поднимается готовая связка Prometheus + Grafana.

### Установка библиотеки метрик

Пакет опубликован на TestPyPI; для локальной разработки:

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ flask-service-metrics
```

Docker-образ вместо этого ставит её из локального wheel
(`wheels/flask_service_metrics-0.1.1-py3-none-any.whl`, подключён строкой в
`requirements.txt`) - сборка не зависит от внешнего индекса. После изменения
библиотеки: пересобрать wheel (`python -m build` в её репозитории),
скопировать в `wheels/` и обновить имя файла в `requirements.txt`.

### Как подключено в приложении

- `app/extensions.py` - `metrics = FlaskMetrics()`; инициализация в фабрике
  через `metrics.init_app(app)`. Для HTTP-метрик больше ничего не нужно:
  они собираются хуками запросов.
- `app/config.py` - `METRICS_NAMESPACE = "taskservice"`; `/metrics` и
  health-endpoint'ы исключены из HTTP-метрик; `METRICS_LOG_FILE` /
  `METRICS_LOG_INTERVAL` берутся из переменных окружения (docker-compose
  настраивает JSONL-дамп в `/tmp/metrics.jsonl` каждые 30 с).
- `app/resources/common.py` - декоратор `@measure` на `get_or_404` как пример
  метрик уровня метода.

### Где смотреть метрики

| Что | Где |
|---|---|
| Дашборд Grafana (понятный человеку вид) | <http://localhost:3000/d/flask-svc-metrics> - вход не требуется |
| Сырой текстовый формат Prometheus | <http://localhost:5001/metrics> |
| Prometheus UI (произвольные запросы) | <http://localhost:9090> |
| JSONL-лог | `docker compose exec app tail /tmp/metrics.jsonl` |

На дашборде: RPS, латентность p95, коды ответов и исключения по endpoint'ам,
частота и длительность SQL по операциям, функции под `@measure`, метрики
процесса (CPU, RSS, потоки, GC); обновление каждые 5 секунд. Prometheus
опрашивает приложение раз в 5 секунд. Чтобы графики ожили, подайте нагрузку:

```bash
for i in $(seq 1 500); do curl -s -o /dev/null http://localhost:5001/projects/; done
```
