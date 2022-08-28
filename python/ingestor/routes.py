import python.common.helper as helper
from python.ingestor.config import Config
from python.common.rabbitmq import RabbitMQ
from flask import request, jsonify, g, Flask
import logging
import logging.config
import json
import uuid
import pytz
from datetime import datetime


application = Flask(__name__)
application.secret = Config.FLASK_SECRET_KEY
logging.config.dictConfig(Config.LOGGING)
logging.warning('*** ingestor initialized and ready for use ***')


@application.before_request
def before_request_function():
    g.writer = RabbitMQ(Config())


@application.route('/department/<department>/form/<form_id>/submit', methods=["POST"])
def ingest(department, form_id):
    # TODO - remove before flight - sanitize url parameters
    if request.method == 'POST':
        args = helper.execute_pipeline(
            [
                {"try": _build_event_from_payload, "fail": [
                    {"try": _unable_to_build_event, "fail": []},
                ]},
                {"try": _add_to_rabbitmq, "fail": [
                    {"try": _unable_to_write_to_rabbitmq, "fail": []},
                ]},
                {"try": _okay, "fail": []}
            ],
            queue=Config.STREAM_NAME,
            writer=g.writer,
            request=request,
            department=department,
            form_id=form_id,
            config=Config)
        return args.get('response')


def _build_event_from_payload(**kwargs) -> tuple:
    r = kwargs.get('request')
    yukon_tz = pytz.timezone("America/Whitehorse")
    try:
        kwargs['event'] = {
            "event": {
                "type": "submission",
                "submission_id": str(uuid.uuid4()),
                "received": datetime.now(yukon_tz).isoformat(),
                "event_version": "0.1.1",
                "department": kwargs.get('department'),
                "form_id": kwargs.get('form_id'),
                "payload": r.json
            }
        }
        return True, kwargs
    except Exception as error:
        logging.warning("failed to build event from from the request: " + str(error))
        return False, kwargs


def _add_to_rabbitmq(**args) -> tuple:
    event = args.get('event')
    queue = args.get('queue')
    writer = args.get('writer')
    logging.info('writing to {} queue'.format(queue))
    if not writer.publish(queue, bytes(json.dumps(event), Config.RABBITMQ_MESSAGE_ENCODING)):
        logging.critical('unable to write to RabbitMQ {} queue'.format(queue))
        return False, args
    return True, args


def _okay(**args) -> tuple:
    args['response'] = jsonify({"message": "received"}), 200
    return True, args


def _unable_to_build_event(**args) -> tuple:
    logging.warning("unable to build event")
    args['response'] = jsonify({"error": "internal system error"}), 500
    return True, args


def _unable_to_write_to_rabbitmq(**args) -> tuple:
    logging.warning("unable to write to RabbitMQ")
    args['response'] = jsonify({"error": "internal system error"}), 500
    return True, args

# def _decode_message(body: bytes, encoding="utf-8") -> dict:
#     message_string = body.decode(encoding)
#     return json.loads(message_string)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
