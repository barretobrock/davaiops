from flask import (
    Flask,
    redirect,
    render_template,
    url_for
)
from flask_admin import (
    Admin,
    helpers as admin_helpers
)
from flask_admin.contrib.sqla import ModelView
from flask_security import (
    current_user,
    Security,
    SQLAlchemyUserDatastore,
    UserMixin
)
from flask_sqlalchemy import SQLAlchemy


# Instantiate the Flask application with configurations
# secure_app = Flask(__name__)
# secure_app.config.update({
#     # Bootswatch theme
#     'FLASK_ADMIN_SWATCH': 'sandstone',
#     'SECRET_KEY': 'secretkey',
#     'SECURITY_PASSWORD_SALT': 'none',
#     # Configure application to route to the Flask-Admin index view upon login/logout/registration
#     'SECURITY_POST_LOGIN_VIEW': '/admin/',
#     'SECURITY_POST_LOGOUT_VIEW': '/admin/',
#     'SECURITY_POST_REGISTER_VIEW': '/admin/',
#     'SECURITY_REGISTERABLE': True,
#     # Configure application to
#     'SECURITY_SEND_REGISTER_EMAIL': False,
#     'SQLALCHEMY_TRACK_MODIFICATIONS': 'False',
#     'SQLALCHEMY_DATABASE_URI': 'postgres://localhost/slackdb',
# })
