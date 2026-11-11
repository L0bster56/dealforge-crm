from dataclasses import dataclass
from uuid import UUID

from src.backend.application.auth.errors import EmailAlreadyExistsError
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.update_user import UpdateUserCommand
from src.backend.application.user.errors import UserNotFoundError, UsernameAlreadyExistsError
from src.backend.domain.user.entity import User
from src.backend.domain.user.policies.can_update import CanUpdateUserPolicy


@dataclass
class UpdateUserUseCase:
    """
    Use Case обновления данных пользователя.

    Отвечает за:
    - получение пользователя по ID
    - проверку существования пользователя
    - проверку прав доступа через policy
    - проверку уникальности email и username
    - обновление данных пользователя через доменные методы
    - сохранение изменений в БД

    Attributes:
        uow: UnitOfWork для доступа к репозиториям.
        actor: пользователь, выполняющий операцию (инициатор действия).
    """

    uow: UnitOfWork
    actor: User

    async def execute(self, user_id: UUID, cmd: UpdateUserCommand) -> None:
        """
        Выполняет обновление пользователя.

        Args:
            user_id: идентификатор пользователя, которого обновляют.
            cmd: команда с новыми данными пользователя.

        Raises:
            UserNotFoundError: если пользователь не найден.
            EmailAlreadyExistsError: если email уже используется.
            UsernameAlreadyExistsError: если username уже используется.
            PermissionError: если actor не имеет прав на обновление.

        Returns:
            None
        """

        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)

            if not user:
                raise UserNotFoundError(
                    f"user with id {user_id} not found"
                )

            CanUpdateUserPolicy(self.actor, user.role).enforce()

            if await self.uow.users.exists_email(cmd.email, user.id):
                raise EmailAlreadyExistsError("email already exists")

            if await self.uow.users.exists_username(cmd.username, user.id):
                raise UsernameAlreadyExistsError("username already exists")

            user.change_first_name(cmd.first_name)
            user.change_last_name(cmd.last_name)
            user.change_email(cmd.email)
            user.change_username(cmd.username)

            await self.uow.users.update(user)
            await self.uow.commit()