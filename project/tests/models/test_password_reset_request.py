from project.models.password_reset_request import PasswordResetRequest
from datetime import datetime


def test_create_password_reset_request(init_database, _db):
    password_reset_request = PasswordResetRequest(email="test@test.com")
    assert password_reset_request.email == "test@test.com"
    password_reset_request.save()
    assert PasswordResetRequest.query.count() == 1
