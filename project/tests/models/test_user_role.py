from project.models.role import Role
from project.models.user import User
from project.models.user_role import UserRole


def test_create_user_role(init_database, _db):
    user = User(uid="test_user")
    role = Role(name="Admin", permissions=["admin", "edit", "view"])
    user_role = UserRole(user_id=user.id, role_id=role.id, user=user, role=role)
    assert user_role
    assert user_role.user_id == user.id
    assert user_role.role_id == role.id

    assert user.roles == [role.id]
    assert role.users == [user]
