from project.controllers.base_controller import BaseController
from project.models.activatable_object import ActivatableObject

class ActivatableObjectController(BaseController):
    """
    Base controller for the Activatable objects.
    Implements generic enable and disable to all Model classes.
    """

    object_class = ActivatableObject
    null_object_class = None

    @classmethod
    def load_active(cls, id: int) -> None:
        """
        Receives an id of a Model object.
        Loads and updates (enables) the object through the base controller method.
        Returns the updated object.
        """
        return cls.load_updated(id=id, active=True)

    @classmethod
    def load_inactive(cls, id: int) -> None:
        """
        Receives an id of a Model object.
        Loads and updates (disables) the object through the base controller method.
        Returns the updated object.
        """
        return cls.load_updated(id=id, active=False)
