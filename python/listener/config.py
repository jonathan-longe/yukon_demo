import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    # See:  https://www.rabbitmq.com/streams.html
    X_STREAM_OFFSET                         = os.getenv('X_STREAM_OFFSET', 'next')
    CALLBACK_FN_NAME                        = os.getenv('CALLBACK_FN_NAME', 'write_to_database')
    DATABASE_API_URI                        = os.getenv('DATABASE_API_URI', 'http://database_api:5000/events')
