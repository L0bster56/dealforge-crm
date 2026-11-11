from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.delete_user import DeleteUserCommand
from src.backend.application.user.errors import UserNotFoundError
from src.backend.domain.user.entity import User
from src.backend.domain.user.policies.can_delete import CanDeleteUserPolicy


@dataclass
class DeleteUserUseCase:
    """
    Use Case удаления пользователя.

    Отвечает за:
    - поиск пользователя по ID
    - проверку существования пользователя
    - проверку прав доступа через policy
    - удаление пользователя из системы

    Attributes:
        uow: UnitOfWork для работы с репозиториями.
        actor: пользователь, выполняющий операцию (инициатор действия).
    """

    uow: UnitOfWork
    actor: User

    async def execute(self, cmd: DeleteUserCommand) -> None:
        """
        Выполняет удаление пользователя.

        Args:
            cmd: команда удаления пользователя (с user_id).

        Raises:
            UserNotFoundError: если пользователь не найден.
            PermissionError: если actor не имеет прав на удаление.

        Returns:
            None
        """

        async with self.uow:
            user = await self.uow.users.get_by_id(cmd.user_id)

            if not user:
                raise UserNotFoundError(
                    f"user with id {cmd.user_id} not found"
                )

            CanDeleteUserPolicy(self.actor, user.role).enforce()

            await self.uow.users.delete(user)
            await self.uow.commit()