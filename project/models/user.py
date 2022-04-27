from project import db
from project.models.base_model import BaseModel
from project.models.user_role import UserRole


class User(BaseModel):
    __tablename__ = "user"

    uid = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    users_roles = db.relationship("UserRole", back_populates="user", lazy="joined")

    @property
    def roles(self):
        return [role.role for role in self.users_roles]

    @property
    def permissions(self):
        aux = set()
        for role in self.roles:
            aux = aux.union(set(role.permissions))
        return list(aux)

    def __repr__(self):
        return f"<User {self.uid}>"

    def __init__(self, uid):
        self.uid = uid
        self.active = True
