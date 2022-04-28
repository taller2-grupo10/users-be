from project.controllers.base_controller import BaseController
from project.models.user_role import UserRole


class UserRoleController(BaseController):
    object_class = UserRole
    null_object_class = None

    @staticmethod
    def _verify_relations(new_user_role: UserRole) -> None:
        """
        No verifications needed.
        """
        pass

    @classmethod
    def load_by_user_id_role_id(cls, user_id, role_id) -> UserRole:
        user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()
        return user_role

    @classmethod
    def create(
        cls,
        user_id,
        role_id,
    ) -> UserRole:
        """
        Receives user_role data and additional arguments.
        Returns a new user_role.
        """
        user_role = UserRoleController.load_by_user_id_role_id(
            user_id=user_id, role_id=role_id
        )
        if not user_role:
            user_role = UserRole(user_id=user_id, role_id=role_id)
            cls.save(user_role)
        # Possible optimization for the future User's role update:
        # Mark every (already created) user_role as undeleted() bc if you have tried to create a Us-Ro
        # that already exists, it's bc you need it again.

        return user_role
