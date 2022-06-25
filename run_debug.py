from flask import (
    render_template,
    request
)
# Internal packages
from davaiops.configurations import DevelopmentConfig
from davaiops.routes import create_app

app = create_app(config_class=DevelopmentConfig)


@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(403)
def handle_err(err):
    app.extensions['loguru'].error(err)
    if err.code == 404:
        app.extensions['loguru'].error(f'Path requested: {request.path}')
    return render_template(f'errors/{err.code}.html'), err.code


if __name__ == "__main__":
    app.run()
