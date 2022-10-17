import os
from python.common.config import Config as BaseConfig


class Config(BaseConfig):
    # See:  https://www.rabbitmq.com/streams.html
    X_STREAM_OFFSET                         = os.getenv('X_STREAM_OFFSET')
    CALLBACK_FN_NAME                        = os.getenv('CALLBACK_FN_NAME', 'echo_to_console')
    DATABASE_API_URI                        = os.getenv('DATABASE_API_URI', 'http://database_api:5000/events')

    MAILGUN_API_KEY                         = os.getenv('MAILGUN_API_KEY')
    MAILGUN_SENDING_URL                     = os.getenv('MAILGUN_SENDING_URL', 'http://mailgun.api/domain/messages')

    EMAIL_FROM_ADDRESS                      = os.getenv('EMAIL_FROM_ADDRESS', 'to_be_determined@yukon.ca')
    EMAIL_SUBJECT                           = os.getenv('EMAIL_SUBJECT', 'A form has been submitted')

    DRUPAL_WEB_ROOT                         = os.getenv('DRUPAL_WEB_ROOT')

    # Dictionary that maps departments and form_id to email recipient.
    # If department, form_id or email address is not listed below, the message will be ignored
    EMAIL_TO_ADDRESS = {
        "eservices": {
            "support": "jlonge@corebox.net",
            "request_for_support": "jlonge@corebox.net",
            "file_attachment_test": "jlonge@corebox.net"
        },
        "health_services": {
            "vaccination_request": "to_be_determined@yukon.ca"
        }
    }
    EMAIL_TEMPLATE_PATH = "/home/appuser/python/listener/templates"
    EMAIL_TEMPLATE_FILENAME = "form_submitted.html"


