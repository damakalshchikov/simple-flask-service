import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/simple-database",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_TITLE = "Simple Flask Service API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    METRICS_NAMESPACE = "taskservice"
    METRICS_EXCLUDE_PATHS = ["/metrics", "/health", "/health/db"]
    METRICS_LOG_FILE = os.environ.get("METRICS_LOG_FILE")
    METRICS_LOG_INTERVAL = float(os.environ.get("METRICS_LOG_INTERVAL", "60"))
