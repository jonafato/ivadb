from flask import Flask
from flask.ext.security import SQLAlchemyUserDatastore

from .core import api, db, security
from .models import User, Role

from .views import bp


def create_app(settings_override=None):
    """Creates and returns a configured :class:`~flask.Flask` application.

    :param package_name: application package name.
    :param settings_override: ``dict`` containing settings to override.
    """
    if settings_override is None:
        settings_override = {}
    app = Flask(__name__)
    app.config.from_object('ivadb.settings')
    app.config.update(settings_override)

    api.init_app(app)
    db.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role))
    app.register_blueprint(bp)
    return app
