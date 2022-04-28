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
        return [ur.role.id for ur in self.users_roles if not ur.is_deleted]

    @roles.setter
    def roles(self, roles_id):
        """
        Receives a list of roles ids.
        For each role_id:
          If user has a role id that is not in the list, the UserRole is deleted.
          If user has that role id set as deleted, the UserRole is undeleted.
          If user doesn't have that role id, a new UserRole is created.
        """
        for ur in self.users_roles:
            if ur.role_id not in roles_id:
                ur.delete()
            elif ur.is_deleted:
                ur.undelete()
        prev_roles = self.roles
        for id in roles_id:
            if id not in prev_roles:
                self.users_roles.append(UserRole(role_id=id, user=self))

    @property
    def permissions(self):
        aux = set()
        for role in self.roles:
            aux = aux.union(set(role.permissions))
        return list(aux)

    def __repr__(self):
        return f"<User {self.uid}>"

    def __init__(self, uid, roles):
        self.uid = uid
        self.active = True
        self.roles = roles
