
def get_schemas() -> dict:
    return {
        "eservices": {
            "report-a-pothole": {
                "email": {
                    "type": "string",
                    'minlength': 4,
                    'maxlength': 40,
                    "required": True
                },
                "location": {
                    "type": "string",
                    'minlength': 4,
                    'maxlength': 70,
                    "required": True
                },
                "affects": {
                    "type": "string",
                    'minlength': 2,
                    'maxlength': 30,
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
