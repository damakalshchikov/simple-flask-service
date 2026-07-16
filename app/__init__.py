from flask import Flask, jsonify
from sqlalchemy import text

from app.config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app import models  # noqa: F401

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/health/db")
    def health_db():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "ok", "db": "connected"})
        except Exception as exc:
            return jsonify({"status": "error", "detail": str(exc)}), 500

    return app
