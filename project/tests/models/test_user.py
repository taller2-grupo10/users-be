from project.models.user import User


def test_create_user(init_database, _db):
    user = User(uid="test_user")
    assert user
    assert user.uid == "test_user"
    assert user.active == True