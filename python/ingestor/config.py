import os
from python.common.config import Config as BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseConfig):
    FLASK_SECRET_KEY                    = os.getenv('FLASK_SECRET_KEY')

    # Routes are protected with         basic http authentication
    FLASK_BASIC_AUTH_USER               = os.getenv('FLASK_BASIC_AUTH_USER')
    FLASK_BASIC_AUTH_PASS               = os.getenv('FLASK_BASIC_AUTH_PASS')
