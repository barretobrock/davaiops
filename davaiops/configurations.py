from pathlib import Path

KEY_DIR = Path().home().joinpath('keys')


def get_local_secret(fpath: Path) -> str:
    """Grabs a locally-stored secret for debugging"""
    with fpath.open('r') as f:
        return f.read().strip()


class Config(object):
    """
    Default config
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/davaidb'
    SECRET_KEY = get_local_secret(KEY_DIR.joinpath('DAVAI_SECRET_KEY'))
    REGISTER_KEY = get_local_secret(KEY_DIR.joinpath('REGISTRATION_KEY'))
    TWILIO_SID = get_local_secret(KEY_DIR.joinpath('TWILIO_SID'))
    TWILIO_TOKEN = get_local_secret(KEY_DIR.joinpath('TWILIO_TOKEN'))
    CALL_ALLOW_LIST = get_local_secret(KEY_DIR.joinpath('CALL_ALLOW_LIST')).split(',')
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
