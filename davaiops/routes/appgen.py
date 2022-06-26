from flask import (
    Flask,
    url_for
)
from pukr import (
    get_logger,
    InterceptHandler
)
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
from davaiops.routes.main import main
from davaiops.routes.projects import projects
from davaiops.routes.user import users


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
    logger = get_logger('davaiops', app.config.get('LOG_DIR'), show_backtrace=True, base_level='DEBUG')
    logger.debug('Logger started. Binding to app handler.')
    app.logger.addHandler(InterceptHandler(logger=logger))
    app.extensions.setdefault('loguru', logger)

    # Register routes
    for rt in [admin, api, koned, main, projects, users]:
        app.register_blueprint(rt)

    return app
