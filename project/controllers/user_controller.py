from project.controllers.base_controller import BaseController
from project.models.user import User
from project.controllers.user_role_controller import UserRoleController


class UserAlreadyExists(Exception):
    pass


class UserController(BaseController):
    object_class = User
    null_object_class = None

    @staticmethod
    def _verify_relations(new_user: User) -> None:
        """
        No verifications needed.
        """
        pass

    @classmethod
    def load_by_uid(cls, uid: str) -> User:
        user = User.query.filter_by(uid=uid).first()
        return user

    @classmethod
    def create(
        cls,
        uid,
        roles,
    ) -> User:
        """
        Receives user data and additional arguments.
        Returns a new user.
        """
        if UserController.load_by_uid(uid):
            raise UserAlreadyExists()
        try:
            roles = list(map(int, roles.split(",")))
        except ValueError:
            raise ValueError("Roles must be integers")

        new_user = User(uid=uid)
        cls.save(new_user)
        for role_id in roles:
            UserRoleController.create(user_id=new_user.id, role_id=role_id)
        return new_user