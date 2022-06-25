import logging
from flask import (
    render_template,
    request
)
# Internal packages
from davaiops.configurations import ProductionConfig
from davaiops.routes import create_app

app = create_app(config_class=ProductionConfig)


@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(403)
def handle_err(err):
    app.extensions['loguru'].error(err)
    if err.code == 404:
        app.extensions['loguru'].error(f'Path requested: {request.path}')
    return render_template(f'errors/{err.code}.html')


if __name__ == "__main__":
    # Set logging based on the --log-level=<level> argument from gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel = gunicorn_logger.level

    app.run()
