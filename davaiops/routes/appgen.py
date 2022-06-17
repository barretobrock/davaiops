import logging
from pathlib import Path
from flask import Flask
from loguru import logger
# Internal packages
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


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


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

    # Set up log path if necessary
    logpath = Path().home().joinpath('logs').joinpath('davaiops')
    logpath.mkdir(parents=True, exist_ok=True)
    # Register logger, bind handler into flask app
    logger.add(
        sink=logpath.joinpath('davaiops.log'),
        level='DEBUG',
        format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | '
               '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
               '<level>{message}</level>',
        enqueue=True,
        rotation='7 days',
        retention='30 days',
    )
    logger.debug('Logger started. Binding to app handler.')
    app.logger.addHandler(InterceptHandler())

    # Register routes
    for rt in [admin, api, koned, main, users, errors]:
        app.register_blueprint(rt)

    return app
