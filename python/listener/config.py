import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    # See:  https://www.rabbitmq.com/streams.html
    X_STREAM_OFFSET                         = os.getenv('X_STREAM_OFFSET', 'next')
    CALLBACK_FN_NAME                        = os.getenv('CALLBACK_FN_NAME', 'echo_to_console')
