from project import db
from project.models.base_model import BaseModel
from project.models.user_role import UserRole


class User(BaseModel):
    __tablename__ = "user"

    uid = db.Column(db.String(128), unique=True, nullable=False)
    artist_id = db.Column(db.String(128), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    users_roles = db.relationship("UserRole", back_populates="user", lazy="joined")

    @property
    def roles(self):
        return [ur.role for ur in self.users_roles if not ur.is_deleted]

    @property
    def permissions(self):
        aux = set()
        for role in self.roles:
            aux = (
                aux.union(set(role.permissions))
                if role.permissions
                else aux.union(set())
            )
        return list(aux)

    def __repr__(self):
        return f"<User {self.uid}>"

    def __init__(self, uid, artist_id):
        self.uid = uid
        self.active = True
        self.artist_id = artist_id

    def _update(self, active=True, **kwargs):
        """
        Particular Enableable object update method.
        """
        if active is not None:
            self.active = active
