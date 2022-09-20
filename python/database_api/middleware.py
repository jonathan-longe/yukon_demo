import json
import logging
from cerberus import Validator
from python.database_api.models import Event, db, RequestForSupport
from datetime import datetime


def request_contains_a_payload(**kwargs) -> tuple:
    request = kwargs.get('request')
    try:
        payload = request.get_json()
        kwargs['payload'] = payload
        logging.debug("payload: " + json.dumps(payload))
    except Exception as e:
        return False, kwargs
    return payload is not None, kwargs


def validate_payload(**kwargs) -> tuple:
    logging.debug("inside validate_payload()")
    message_dict = kwargs.get('payload')
    schema = kwargs.get('validation_schemas')[message_dict['event']['department']][message_dict['event']['form_id']]
    logging.warning(json.dumps(schema))
    logging.warning(json.dumps(message_dict['event']['payload']))
    v = Validator(schema)
    v.allow_unknown = False
    if v.validate(message_dict['event']['payload']):
        return True, kwargs
    logging.warning("validation error: " + json.dumps(v.errors))
    kwargs['validation_errors'] = v.errors
    return False, kwargs


def create_or_update_the_event(**kwargs) -> tuple:
    logging.debug("inside create_or_update_the_event()")
    payload = kwargs.get('payload')
    try:
        event = Event(
            submission_id=payload['event']['submission_id'],
            form_type=payload['event']['type'],
            version=payload['event']['event_version'],
            department=payload['event']['department'],
            form_id=payload['event']['form_id'],
            received=datetime.strptime(payload['event']['received'], "%Y-%m-%d %H:%M:%S")
        )
        db.session.merge(event)
        db.session.commit()
    except Exception as e:
        logging.warning("error create_or_update_the_event()" + str(e))
        kwargs['error'] = str(e)
        return False, kwargs
    return True, kwargs


def create_or_update_the_payload(**kwargs) -> tuple:
    logging.debug("inside create_or_update_the_payload()")
    payload = kwargs.get('payload')
    department = payload['event']['department']
    form_id = payload['event']['form_id']
    logging.warning(str(payload))
    try:
        model = _save_payload(payload['event']['submission_id'], payload['event']['payload'])[department][form_id]
        db.session.merge(model)
        db.session.commit()
    except Exception as e:
        logging.warning("error create_or_update_the_payload()" + str(e))
        kwargs['error'] = str(e)
        return False, kwargs
    return True, kwargs


def _save_payload(submission_id, payload):
    return {
        "eservices": {
            "request_for_support": RequestForSupport(
                submission_id=submission_id,
                urgent=payload.get('urgent'),
                description_of_the_problem=payload.get('description_of_the_problem'),
                first_name=payload.get('first_name'),
                last_name=payload.get('last_name'),
                remote_addr=payload.get('remote_addr')
            )
        }
    }
