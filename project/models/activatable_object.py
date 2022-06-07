from project import db
from project.models.base_model import BaseModel


class ActivatableObject(BaseModel):
    """
    Interface for object with capability to be enabled and disabled.
    """

    __abstract__ = True
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def _update(self, active=None, **kwargs):
        """
        Particular Enableable object update method.
        """
        if active is not None:
            self.active = active