import pytest
from python.database_api import create_app
from python.database_api.config import TestConfig
from python.database_api.models import db


@pytest.fixture
def application():
    return create_app(TestConfig)


@pytest.fixture
def as_guest(application):
    with application.test_client() as client:
        yield client


@pytest.fixture
def database(application):
    with application.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
