from project import db
from project.models.base_model import BaseModel
from project.models.user_role import UserRole


class User(BaseModel):
    __tablename__ = "user"

    uid = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    artist_id = db.Column(db.String(128), nullable=True)
    notification_token = db.Column(db.String(128), nullable=True)
    wallet_id = db.Column(db.BIGINT(), nullable=True)

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

    def __init__(self, uid, artist_id=None, notification_token=None, wallet_id=None):
        self.uid = uid
        self.active = True
        self.artist_id = artist_id
        self.notification_token = notification_token
        self.wallet_id = wallet_id

    def _update(self, **kwargs):
        """
        Particular object update method.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
