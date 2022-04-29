from project.models.role import Role


def test_create_role(init_database, _db):
    role = Role(name="Admin", permissions=["admin", "edit", "view"])
    assert role.name == "Admin"
    assert role.permissions == ["admin", "edit", "view"]
