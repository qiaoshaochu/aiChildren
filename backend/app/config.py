import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///children_growth.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def init_config(app):
    app.config.from_object(Config)


__all__ = ["Config", "init_config"]

