
class Validation:

    # Drupal payload must contain "sid" and "uri" fields for linking back to form submission
    REQUIRED_FIELDS_FOR_EMAILING = {
        "type": {
            "type": "string",
            "required": True
        },
        "payload": {
            "type": "dict",
            "required": True,
            "schema": {
                "sid": {
                    "type": "string",
                    "required": True
                },
                "uri": {
                    "type": "string",
                    "required": True
                }
            }
        },
    }
