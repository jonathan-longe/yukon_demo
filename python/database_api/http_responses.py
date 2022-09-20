from flask import make_response


def successful_create_response(**kwargs) -> tuple:
    response_dict = kwargs.get('response_dict', {
        "message": "create successful"
    })
    kwargs['response'] = make_response(response_dict, 200)
    return True, kwargs


def successful_update_response(**kwargs) -> tuple:
    response_dict = kwargs.get('response_dict', {
        "message": "update successful"
    })
    kwargs['response'] = make_response(response_dict, 200)
    return True, kwargs


def server_error_response(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': kwargs.get("error")}, 500)
    return True, kwargs


def payload_missing(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'missing payload'}, 403)
    return True, kwargs


def failed_validation(**kwargs) -> tuple:
    kwargs['response'] = make_response({
        'message': 'failed validation',
        'errors': kwargs.get('validation_errors')
    }, 400)
    return True, kwargs