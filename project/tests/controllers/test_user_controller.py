from project.models.user import User
from project.controllers.user_controller import UserController


def test_create_user(init_database, _db, role):
    user = UserController.create(
        uid="test_user",
        role_id=role.id,
        artist_id="1",
        notification_token="123",
        wallet_id="456",
    )

    assert user.uid == "test_user"
    assert user.artist_id == "1"
    assert user.notification_token == "123"
    assert user.active == True
    assert user.created_at is not None
    assert user.updated_at is None
    assert user.is_deleted == False
    assert user.id is not None
    assert user.uid is not None
    assert user.artist_id is not None
    assert user.notification_token is not None
    assert user.wallet_id is not None
    assert user.roles == [role]
    assert role.users == [user]
    assert set(user.permissions) == set(role.permissions)


def test_load_by_uid(init_database, _db, user):
    user_loaded = UserController.load_by_uid(user.uid)
    assert user == user_loaded


def test_load_by_artist_id(init_database, _db, user):
    user_loaded = UserController.load_by_artist_id(user.artist_id)
    assert user == user_loaded


def test_update_user(init_database, _db, user):
    UserController._update(
        user, uid="test_user_updated", artist_id="2", notification_token="456"
    )

    updated_user = User.query.first()
    assert updated_user.uid == "test_user_updated"
    assert updated_user.artist_id == "2"
    assert updated_user.notification_token == "456"
    assert updated_user.active == True
    assert updated_user.created_at is not None
    assert updated_user.updated_at is not None
    assert updated_user.is_deleted == False
    assert updated_user.id is not None
    assert updated_user.uid is not None
    assert updated_user.artist_id is not None
    assert updated_user.notification_token is not None


def test_load_by_id(init_database, _db, user):
    user_loaded = UserController.load_by_id(user.id)
    assert user == user_loaded


def test_load_all(init_database, _db, user, role):
    new_user = UserController.create(
        uid="test_user_2",
        role_id=role.id,
        artist_id="2",
        notification_token="456",
        wallet_id="789",
    )

    users = UserController.load_all()
    assert len(users) == 2
    assert user in users
    assert new_user in users


def test_delete_user(init_database, _db, user):
    UserController.delete(user.id)
    assert user.is_deleted == True


def test_load_updated(init_database, _db, user):
    user_loaded = UserController.load_updated(user.id, uid="NEW UID")
    assert user == user_loaded
    assert user_loaded.uid == "NEW UID"
