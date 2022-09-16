from python.database_api.config import Config
from flask import request, Blueprint, make_response
from python.common.helper import execute_pipeline
import python.database_api.http_responses as http_responses
from python.database_api.validation_schema import get_schemas
import python.database_api.middleware as mw
from flask_cors import CORS
import logging.config

logging.config.dictConfig(Config.LOGGING)
logging.info('*** database adapter blueprint loaded ***')

bp = Blueprint('event', __name__, url_prefix=Config.URL_PREFIX)
CORS(bp, resources={Config.URL_PREFIX + "/events": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/events', methods=['POST'])
def post_event():
    if request.method == 'POST':
        kwargs = execute_pipeline([
            {"try": mw.request_contains_a_payload, "fail": [
                {"try": http_responses.payload_missing, "fail": []},
            ]},
            {"try": mw.validate_payload, "fail": [
                {"try": http_responses.failed_validation, "fail": []},
            ]},
            {"try": mw.create_or_update_the_event, "fail": [
                {"try": http_responses.server_error_response, "fail": []},
            ]},
            {"try": mw.create_or_update_the_payload, "fail": [
                {"try": http_responses.server_error_response, "fail": []},
            ]},
            {"try": http_responses.successful_create_response, "fail": []},
            ],
            validation_schemas=get_schemas(),
            request=request,
            config=Config)
        return kwargs.get('response')
