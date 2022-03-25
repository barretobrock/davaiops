from flask import (
    render_template,
    Blueprint
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
