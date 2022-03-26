from flask import (
    render_template,
    Blueprint,
    Response
)

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    return render_template('index.html')


@main.route('/projects')
def projects():
    return render_template('projects/projects.html', title='Projects')


@main.route('/contact')
def contact() -> str:
    return render_template('contact.html', title='Contact')


@main.route('/robots.txt')
def robots() -> Response:
    """Responds with robots.txt instructions to discourage web crawling"""
    resp = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp
