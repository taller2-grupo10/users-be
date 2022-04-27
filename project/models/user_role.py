from project import db
from project.models.base_model import BaseModel


class UserRole(BaseModel):
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True)

    user = db.relationship("User", back_populates="users_roles")
    role = db.relationship("Role", back_populates="_users")

    def __repr__(self):
        return f"<UserRole {self.user_id} {self.role_id}>"
