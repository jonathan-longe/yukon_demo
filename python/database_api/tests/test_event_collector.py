import responses
from python.database_api.config import Config
from python.database_api.models import Event, RequestForSupport


@responses.activate
def test_an_event_can_be_submitted_to_the_collector(as_guest, database):
    resp = as_guest.post(Config.URL_PREFIX + "/events",
                         content_type="application/json",
                         json=_get_valid_event())
    assert resp.status_code == 200
    assert database.session.query(Event).filter(Event.id == "aaaa-bbbb-cccc-dddd").count() == 1
    assert database.session.query(RequestForSupport).filter(RequestForSupport.id == "aaaa-bbbb-cccc-dddd").count() == 1


def _get_valid_event() -> dict:
    return {
        "event": {
            "type": "submission",
            "submission_id": "aaaa-bbbb-cccc-dddd",
            "received": "2022-09-02 15:02:03",
            "event_version": "0.1.1",
            "department": "eservices",
            "form_id": "request_for_support",
            "payload": {
                "remote_addr": "199.45.12.13",
                "description_of_the_problem": "need help creating digital form",
                "first_name": "Joe",
                "last_name": "Smith",
                "urgent": "yes"
            }
        }
    }
