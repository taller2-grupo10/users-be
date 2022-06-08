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
        role_id,
        artist_id,
        notification_token,
    ) -> User:
        """
        Receives user data and additional arguments.
        Returns a new user.
        """
        new_user = User(
            uid=uid, artist_id=artist_id, notification_token=notification_token
        )
        cls.save(new_user)
        UserRoleController.create(user_id=new_user.id, role_id=role_id)
        return new_user
