import logging
from flask import Flask
# Internal packages
from davaiops.logg import get_base_logger
from davaiops.configurations import BaseConfig
from davaiops.flask_base import (
    db,
    bcrypt,
    log_mgr
)
from davaiops.routes.admin import admin
from davaiops.routes.api import api
from davaiops.routes.koned import koned
from davaiops.routes.errors import errors
from davaiops.routes.main import main
from davaiops.routes.user import users


logger = get_base_logger()


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def create_app(*args, **kwargs) -> Flask:
    """Creates a Flask app instance"""
    # Config app
    config_class = kwargs.pop('config_class', BaseConfig)
    app = Flask(__name__, static_folder=config_class.STATIC_DIR_PATH,
                template_folder=config_class.TEMPLATE_DIR_PATH)
    app.config.from_object(config_class)
    # Initialize things that supports app
    db.init_app(app)
    bcrypt.init_app(app)
    log_mgr.init_app(app)

    # Register logger, bind handler into flask app
    app.logger.addHandler(InterceptHandler())

    # Register routes
    for rt in [admin, api, koned, main, users, errors]:
        app.register_blueprint(rt)

    return app
