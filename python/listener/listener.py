from python.listener.config import Config
from python.common.rabbitmq import RabbitMQ
from cerberus import Validator as Cerberus
from jinja2 import Environment, FileSystemLoader, select_autoescape
from validation_schema import Validation
import logging
import logging.config
import json
import requests

logging.config.dictConfig(Config.LOGGING)


class Listener:
    """
        This listener watches the RabbitMQ stream defined in the
        config.  When a message appears the Listener invokes the
        callback function to handle the event
    """
    def __init__(self, config, rabbit_listener):
        self.config = config
        self.listener = rabbit_listener
        logging.warning('*** listener initialized and ready ***')

    def main(self):
        callback_function = getattr(Listener, Config.CALLBACK_FN_NAME)
        self.listener.consume(self.config.STREAM_NAME, callback_function, self.config.X_STREAM_OFFSET)

    @staticmethod
    def echo_to_console(ch, method, properties, body):
        """
        Callback function
        """
        message_dict = Listener._decode_message(body)
        logging.warning(json.dumps(message_dict, indent=4, sort_keys=False))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def write_to_database(ch, method, properties, body):
        """
        Callback function
        """
        message_dict = Listener._decode_message(body)
        r = requests.post(Config.DATABASE_API_URI, json=message_dict)
        if r.status_code != 200:
            logging.warning(r.reason + " - " + str(r.status_code))
            logging.warning(r.text)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def send_via_email(ch, method, properties, body):
        """
        Callback function
        """
        message_dict = Listener._decode_message(body)
        event = message_dict.get('event', {})
        cerberus = Cerberus(Validation.REQUIRED_FIELDS_FOR_EMAILING)
        cerberus.allow_unknown = True
        if cerberus.validate(event):
            department = event.get('department')
            form_id = event.get('form_id')
            email_to_address = Config.EMAIL_TO_ADDRESS.get(department, {}).get(form_id, None)
            if email_to_address:
                template_env = Environment(
                    loader=FileSystemLoader(searchpath=Config.EMAIL_TEMPLATE_PATH),
                    autoescape=select_autoescape()
                                           )
                template = template_env.get_template(Config.EMAIL_TEMPLATE_FILENAME)
                is_success, response = Listener._send_to_mailgun(
                    Config.MAILGUN_API_KEY,
                    Config.MAILGUN_SENDING_URL,
                    Config.EMAIL_FROM_ADDRESS,
                    email_to_address,
                    Config.EMAIL_SUBJECT,
                    template.render(event)
                )
                if is_success:
                    logging.warning(json.dumps(response) + " " + str(is_success))
                else:
                    logging.warning("unable to send to Mailgun: ", response)
            else:
                logging.warning("no recipient email address found - ignoring")
        else:
            logging.warning("message failed validation: " + json.dumps(cerberus.errors))
            logging.warning("message that failed: " + json.dumps(event, indent=3))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def _decode_message(body: bytes) -> dict:
        message_string = body.decode(Config.RABBITMQ_MESSAGE_ENCODING)
        return json.loads(message_string)

    @staticmethod
    def _send_to_mailgun(api_key: str, url: str, mail_from: str, mail_to: list, subject: str, html: str) -> tuple:
        resp = requests.post(
            url,
            auth=("api", api_key),
            data={"from": mail_from,
                  "to": mail_to,
                  "subject": subject,
                  "html": html})
        if resp.status_code == 200:
            return True, resp.json()
        else:
            return False, {"error": resp.text}


if __name__ == "__main__":
    Listener(
        Config(),
        RabbitMQ(Config()),
    ).main()
