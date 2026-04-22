from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import UserRole, User


class CanUpdateUserPolicy(Policy):
    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(
            self,
            actor: User,
            role: UserRole
    ):
        self._actor = actor
        self._role = role

    def is_satisfied_by(self) -> bool:
        return (
                self._actor.role in self.ALLOWED_ROLES
        ) and (
            self._actor.role == UserRole.admin or
            (self._actor == UserRole.director and self._role != UserRole.admin)
        )

    def _error_message(self) -> str:
        return f"You don't have permission to update user with role: {self._role}"