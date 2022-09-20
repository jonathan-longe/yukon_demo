import os
from python.common.config import Config as BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseConfig):
    SECRET_KEY                          = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS      = False
    DEBUG                               = False
    TESTING                             = False
    LOG_LEVEL                           = "DEBUG"
    SQLALCHEMY_DATABASE_URI             = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    MIGRATION_DIRECTORY                 = "python/database_api/migrations/"

    URL_PREFIX = os.getenv('URL_PREFIX', '')  # no trailing slash!

    # URL of requesting resource
    ACCESS_CONTROL_ALLOW_ORIGIN = os.getenv('ACCESS_CONTROL_ALLOW_ORIGIN', '*')


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'
    SECRET_KEY = 'some-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'