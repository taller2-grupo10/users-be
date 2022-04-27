import pytest
from flask import testing
from project import create_app, db
from werkzeug.datastructures import Headers

"""
How to use pytest.fixture defined here:

When writting tests, if you add as a parameter the function name (e.g. test_client)
then before the test runs, the test_client function will run and in the parameter
you will be able to manipulate the yielded object (in this case the CustomTestClient)
"""

### DB Setup ###


class CustomTestClient(testing.FlaskClient):
    """
    Custom client to add
    """

    def __init__(self, *args, **kwargs) -> None:
        self.custom_token = None
        super().__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        if self.custom_token:
            api_key_headers = Headers({"Authorization": f"Bearer {self.custom_token}"})
            headers = kwargs.pop("headers", Headers())
            headers.extend(api_key_headers)
            kwargs["headers"] = headers
        return super().open(*args, **kwargs)

    def set_auth_token(self, token):
        self.custom_token = token


@pytest.fixture(scope="function")
def test_client():
    flask_app = create_app("project.config.ConfigTest")
    flask_app.test_client_class = CustomTestClient
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="function")
def init_database(test_client):
    # Create the database and the database table
    db.create_all()
    yield db  # Test
    db.drop_all()


@pytest.fixture(scope="function")
def _db():
    return db


### Fixture defines ###
