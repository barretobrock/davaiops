import base64
import os
import time
from datetime import (
    datetime,
    timedelta
)
from dataclasses import dataclass
import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    VARCHAR
)
from sqlalchemy.orm import deferred
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
# Local
from davaiops.flask_base import (
    db,
    log_mgr
)


@log_mgr.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


@dataclass
class User(db.Model, UserMixin):

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50), unique=True, nullable=False)
    # This makes the column rendered only when calling it directly
    password_hash = deferred(Column(VARCHAR(128)))
    token = Column(VARCHAR(32), index=True, unique=True)
    token_expiration = Column(TIMESTAMP, default=datetime.now())

    def __init__(self, username: str, password_hash: str, user_id: int = None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_s: int = 1800):
        return jwt.encode({
            'reset_password': self.id, 'exp': time.time() + expires_s
        }, key=current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token: str):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['reset_password']
        except Exception as _:
            return
        return User.query.get(user_id)

    def get_token(self, expires_in: int = 3600):
        now = datetime.utcnow()
        if self.token is not None and self.token_expiration > now + timedelta(seconds=expires_in):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    @staticmethod
    def check_token(token: str):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def __repr__(self):
        return f'<User({self.username})>'
