from datetime import datetime
from project import db


class BaseModel(db.Model):
    """
    Abstract.
    Minimum behavior needed by every model/database object
    """

    name = None
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)

    def __bool__(self) -> bool:
        return True

    def delete(self) -> None:
        """
        Updates object with deletion status.
        """
        self.update(is_deleted=True)

    def undelete(self) -> None:
        """
        Updates object with deletion status.
        """
        self.update(is_deleted=False)

    def _update(self, **kwargs) -> None:
        """Custom update for each model object attributes"""
        raise NotImplementedError

    def update(self, is_deleted=None, **kwargs) -> None:
        """
        Base update method. Calls the implemented _update method for the implemented
        particular model update.
        """
        self._update(**kwargs)
        self.is_deleted = is_deleted if is_deleted is not None else self.is_deleted
        self.updated_at = datetime.now()


class NullBaseModel(db.Model):
    """
    Null pattern for every BaseModel instance
    """

    __abstract__ = True

    def __bool__(self) -> bool:
        return False
