from project import db
from project.models.base_model import BaseModel


class PasswordResetRequest(BaseModel):
    """
    Password reset request model.
    """

    __tablename__ = "password_reset_requests"
    email = db.Column(db.String(255), nullable=False)

    def __init__(self, email=""):
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()
