import os
key_dir = os.path.abspath('/home/bobrock/keys/')


def get_local_secret(path: str) -> str:
    """Grabs a locally-stored secret for debugging"""
    with open(path) as f:
        return f.read().strip()


class Config(object):
    """
    Default config
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgres://localhost/davaidb'
    SECRET_KEY = get_local_secret(os.path.join(key_dir, 'DAVAI_SECRET_KEY'))
    REGISTER_KEY = get_local_secret(os.path.join(key_dir, 'REGISTRATION_KEY'))
    STATIC_DIR_PATH = '../static'
    TEMPLATE_DIR_PATH = '../templates'


class BaseConfig(Config):
    """
    Base config class
    """
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    """
    Production-specific config
    """
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """
    Development-specific config
    """
    DEBUG = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True
