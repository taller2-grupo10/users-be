from project import db
from project.models.base_model import BaseModel
from sqlalchemy.dialects import postgresql
from project.models.user_role import UserRole


class Role(BaseModel):
    __tablename__ = "role"

    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.Column(postgresql.ARRAY(db.String()), default=[])

    _users = db.relationship("UserRole", back_populates="role", lazy="joined")

    @property
    def users(self):
        return [user.user for user in self._users]

    def __repr__(self):
        return f"<Role {self.name}>"

    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions
