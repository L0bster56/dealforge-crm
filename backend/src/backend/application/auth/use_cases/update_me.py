from dataclasses import dataclass

from src.backend.application.auth.dtos.update_me import UpdateMeCommand
from src.backend.application.auth.errors import EmailAlreadyExistsError
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User


@dataclass
class UpdateMeUseCase:
    """
    UseCase: обновление профиля текущего пользователя.

    Ответственность:
        - Проверка уникальности email
        - Обновление данных пользователя
        - Сохранение изменений в базе данных
    """

    uow: UnitOfWork
    user: User

    async def execute(self, cmd: UpdateMeCommand) -> None:
        """
        Обновляет данные текущего пользователя.

        Args:
            cmd (UpdateMeCommand): новые данные пользователя

        Raises:
            EmailAlreadyExistsError: если email уже используется другим пользователем
        """

        async with self.uow:

            exists = await self.uow.users.exists_email(
                str(cmd.email),
                self.user.id,
            )

            if exists:
                raise EmailAlreadyExistsError(
                    "email already exists"
                )

            self.user.change_first_name(cmd.first_name)
            self.user.change_last_name(cmd.last_name)
            self.user.change_email(str(cmd.email))

            await self.uow.users.update(self.user)
            await self.uow.commit()