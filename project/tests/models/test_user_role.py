from project.models.role import Role
from project.models.user import User
from project.models.user_role import UserRole


def test_create_user_role(init_database, _db):
    user = User(uid="test_user", artist_id="1")
    role = Role(name="Admin", permissions=["admin", "edit", "view"])
    user_role = UserRole(user=user, role=role)
    _db.session.add(user)
    _db.session.add(role)
    _db.session.add(user_role)
    _db.session.commit()

    assert user_role
    assert user_role.user_id == user.id
    assert user_role.role_id == role.id

    assert user.roles == [role]
    assert role.users == [user]
    assert set(user.permissions) == set(role.permissions)
