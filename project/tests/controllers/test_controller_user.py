from project.models.user import User
from project.controllers.user_controller import UserController


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
