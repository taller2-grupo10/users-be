from project.models.role import Role
import pytest


def test_create_role(init_database, _db):
    role = Role(name="Admin", permissions=["admin", "edit", "view"])
    assert role.name == "Admin"
    assert role.permissions == ["admin", "edit", "view"]
    assert role.__repr__() == "<Role Admin>"


def test_delete_role_raises_error(init_database, _db):
    role = Role(name="Admin", permissions=["admin", "edit", "view"])
    with pytest.raises(NotImplementedError):
        role.delete()
        role.name = "Admin"
        role.permissions = ["admin", "edit", "view"]
        role.save()
