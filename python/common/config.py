import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOG_FORMAT                          = "%(asctime)s::%(levelname)s::%(name)s::%(message)s"
    LOG_LEVEL                           = os.environ.get('LOG_LEVEL', 'WARNING').upper()

    RABBITMQ_HOST                       = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_USER                       = os.getenv('RABBITMQ_USER')
    RABBITMQ_PASS                       = os.getenv('RABBITMQ_PASS')
    RABBITMQ_PORT                       = os.getenv('RABBITMQ_PORT', '5672')
    RABBITMQ_EXCHANGE                   = os.getenv('RABBITMQ_EXCHANGE', '')
    MAX_CONNECTION_RETRIES              = os.getenv('MAX_CONNECTION_RETRIES', 25)
    RETRY_DELAY                         = os.getenv('RETRY_DELAY', 30)
    RABBITMQ_MESSAGE_ENCODING           = 'utf-8'

    STREAM_NAME                         = 'forms'

    # OpenShift Environment (dev, test, prod)
    ENVIRONMENT                         = os.getenv('ENVIRONMENT', 'dev')

    LOGGERS_IN_USE = os.getenv('LOGGERS_IN_USE', 'console').split()
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'brief': {
                'format': LOG_FORMAT
            }
        },
        'handlers': {
            'console': {
                'level': LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'brief'
            }
        },
        'loggers': {
            '': {
                'handlers': LOGGERS_IN_USE,
                'level': LOG_LEVEL
            }
        }
    }


