from backend.domain.shared.policy import Policy
from backend.domain.user.entity import User, UserRole


class CanDeleteFunnelPolicy(Policy):
    """
    Политика удаления воронки (Funnel).

    Определяет, может ли пользователь удалить воронку.

    Attributes:
        _actor: Пользователь, выполняющий действие.
    """

    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User):
        """
        Инициализация политики.

        Args:
            actor: Пользователь, который пытается удалить воронку.
        """
        self._actor = actor

    def _error_message(self) -> str:
        """
        Сообщение об ошибке при отказе.

        Returns:
            Текст ошибки.
        """
        return "У вас нет прав на удаление воронки"

    def is_satisfied_by(self) -> bool:
        """
        Проверяет, разрешено ли действие.

        Returns:
            True, если пользователь имеет доступ, иначе False.
        """
        return self._actor.role in self.ALLOWED_ROLES