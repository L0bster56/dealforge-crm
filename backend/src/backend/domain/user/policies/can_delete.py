from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import UserRole, User


class CanDeleteUserPolicy(Policy):
    """
    Политика удаления пользователя.

    Правила:
        - Удалять пользователей могут только admin и director
        - Admin может удалять всех
        - Director не может удалять admin
    """

    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User, role: UserRole):
        self._actor = actor
        self._role = role

    def is_satisfied_by(self) -> bool:
        """
        Проверяет возможность удаления пользователя.

        Returns:
            bool: True если разрешено, иначе False
        """
        return (
                self._actor.role in self.ALLOWED_ROLES
                and (
                        self._actor.role == UserRole.admin
                        or (
                                self._actor.role == UserRole.director
                                and self._role != UserRole.admin
                        )
                )
        )

    def _error_message(self) -> str:
        return f"Недостаточно прав для удаления пользователя с ролью: {self._role}"
