from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    Blueprint
)
from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required
)
# Internal packages
from davaiops.flask_base import (
    db,
    bcrypt
)
from davaiops.model import User
from davaiops.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    ResetPasswordForm
)

users = Blueprint('users', __name__)


@users.route("/register", methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'alert-success')
        return redirect(url_for('users.login'))
    return render_template('auth/register.html', title='Register', form=form)


@users.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'alert-danger')
    return render_template('auth/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account", methods=('GET', 'POST'))
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'alert-success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('auth/account.html', title='Account', form=form)


@users.route("/reset_password/<token>", methods=('GET', 'POST'))
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'alert-warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'alert-success')
        return redirect(url_for('users.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)
