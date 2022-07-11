from project.models.user import User


def test_create_user(init_database, _db):
    user = User(uid="test_user", artist_id="1", notification_token="")
    assert user
    assert user.uid == "test_user"
    assert user.active == True
    assert user.__repr__() == "<User test_user>"


def test_delete_user(init_database, _db):
    user = User(uid="test_user", artist_id="1", notification_token="")
    user.delete()
    assert user.is_deleted == True


def test_undelete_user(init_database, _db):
    user = User(uid="test_user", artist_id="1", notification_token="")
    user.delete()
    assert user.is_deleted == True
    user.undelete()
    assert user.is_deleted == False
