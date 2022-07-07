from project.controllers.user_role_controller import UserRoleController


def test_create_user_role(init_database, _db, user, role):
    user_role = UserRoleController.create(user_id=user.id, role_id=role.id)
    assert user_role
    assert user_role.user_id == user.id
    assert user_role.role_id == role.id

    assert user.roles == [role]
    assert role.users == [user]
    assert set(user.permissions) == set(role.permissions)
    assert user_role.__repr__() == "<UserRole 1 1>"


def test_load_load_by_user_id_and_role_id(init_database, _db, user_role, user, role):

    user_role = UserRoleController.load_by_user_id_role_id(
        user_id=user.id, role_id=role.id
    )
    assert user_role
    assert user_role.user_id == user.id
    assert user_role.role_id == role.id

    assert user.roles == [role]
    assert role.users == [user]
    assert set(user.permissions) == set(role.permissions)
    assert user_role.__repr__() == "<UserRole 1 1>"
