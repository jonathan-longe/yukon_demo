import python.common.helper as helper
from python.ingestor.config import Config
from python.common.rabbitmq import RabbitMQ
from flask import request, jsonify, g, Flask
import logging
import logging.config
import json


application = Flask(__name__)
application.secret = Config.FLASK_SECRET_KEY
logging.config.dictConfig(Config.LOGGING)
logging.warning('*** ingestor initialized ***')


@application.before_request
def before_request_function():
    g.writer = RabbitMQ(Config())


@application.route('/submit', methods=["POST"])
def ingest():
    if request.method == 'POST':
        logging.info("ingestor received data: {} | {}".format(request.remote_addr, request.get_data()))
        args = helper.execute_pipeline(
            [
                {"try": _convert_json_to_dict, "fail": [
                    {"try": _server_error, "fail": []},
                ]},
                {"try": _add_to_rabbitmq, "fail": [
                    {"try": _server_error, "fail": []},
                ]},
                {"try": _okay, "fail": []}
            ],
            queue=Config.STREAM_NAME,
            writer=g.writer,
            request=request,
            config=Config)
        return args.get('response')


def _convert_json_to_dict(**kwargs) -> tuple:
    r = kwargs.get('request')
    try:
        kwargs['payload'] = r.json
        return True, kwargs
    except Exception as error:
        logging.warning("failed to get json from request", str(error))
        return False, kwargs


def _add_to_rabbitmq(**args) -> tuple:
    payload = args.get('payload')
    queue = args.get('queue')
    writer = args.get('writer')
    logging.info('writing to {} queue'.format(queue))
    if not writer.publish(queue, bytes(json.dumps(payload), Config.RABBITMQ_MESSAGE_ENCODING)):
        logging.critical('unable to write to RabbitMQ {} queue'.format(queue))
        return False, args
    return True, args


def _okay(**args) -> tuple:
    args['response'] = jsonify({"message": "received"}), 200
    return True, args


def _server_error(**args) -> tuple:
    # override the error string, we don't want to share too much externally
    args['response'] = jsonify({"error": "internal system error"}), 500
    return True, args


# def _decode_message(body: bytes, encoding="utf-8") -> dict:
#     message_string = body.decode(encoding)
#     return json.loads(message_string)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
