import os

from flask import Flask
from sqlalchemy.orm import DeclarativeBase

from .config import Config
from .extensions import db, mail
from .filters import datetime_format


class Base(DeclarativeBase):
    pass


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .core.routes import core

    # routes
    app.register_blueprint(core)

    # filters
    app.jinja_env.filters["datetime_format"] = datetime_format

    # extensions
    mail.init_app(app)
    db.init_app(app)

    return app
