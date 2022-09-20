
def get_schemas() -> dict:
    return {
        "eservices": {
            "request_for_support": {
                "urgent": {
                    "type": "string",
                    'minlength': 2,
                    'maxlength': 3,
                    "required": True
                },
                "description_of_the_problem": {
                    "type": "string",
                    'minlength': 4,
                    'maxlength': 255,
                    "required": True
                },
                "remote_addr": {
                    "type": "string",
                    'minlength': 7,
                    'maxlength': 20,
                    "required": True
                },
                "first_name": {
                    "type": "string",
                    'minlength': 2,
                    'maxlength': 30,
                    "required": True
                },
                "last_name": {
                    "type": "string",
                    'minlength': 2,
                    'maxlength': 30,
                    "required": True,
                }
            }
        }

    }
