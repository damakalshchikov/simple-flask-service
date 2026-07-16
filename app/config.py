import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/simple-database",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
