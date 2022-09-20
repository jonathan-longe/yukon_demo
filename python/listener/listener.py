from python.listener.config import Config
from python.common.rabbitmq import RabbitMQ
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
        logging.warning('*** form handler initialized and listening ***')

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
    def _decode_message(body: bytes) -> dict:
        message_string = body.decode(Config.RABBITMQ_MESSAGE_ENCODING)
        return json.loads(message_string)


if __name__ == "__main__":
    Listener(
        Config(),
        RabbitMQ(Config()),
    ).main()
