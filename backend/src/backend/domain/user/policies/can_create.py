from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import UserRole, User


class CanCreateUserPolicy(Policy):
    """
    Политика, определяющая возможность создания пользователя.

    Правила:
        - Создавать пользователей могут только admin и director
        - Admin может создавать пользователей с любой ролью
        - Director НЕ может создавать admin
    """

    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User, role: UserRole):
        """
        Args:
            actor (User): Пользователь, выполняющий действие
            role (UserRole): Роль создаваемого пользователя
        """
        self._actor = actor
        self._role = role

    def is_satisfied_by(self) -> bool:
        """
        Проверяет, может ли пользователь создать другого пользователя.

        Returns:
            bool: True если разрешено, иначе False
        """
        return (
                self._actor.role in self.ALLOWED_ROLES
        )and (
                (self._role == UserRole.admin) or
                (self._role == UserRole.director and self._role == UserRole.admin)
            )


    def _error_message(self) -> str:
        return f"Недостаточно прав для создания пользователя с ролью: {self._role}"
