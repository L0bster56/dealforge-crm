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
    uow: UnitOfWork
    actor: User

    async def execute(
            self,
            user_id: UUID,
            cmd: UpdateUserCommand
    ):
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(f"user with id {user_id} not found")

            CanUpdateUserPolicy(self.actor, user.role).enforce()

            exists_email = await self.uow.users.exists_email(cmd.email, user.id)
            if exists_email:
                raise EmailAlreadyExistsError("email already exists")

            exists_username = await self.uow.users.exists_username(cmd.username, user.id)
            if exists_username:
                raise UsernameAlreadyExistsError("username already exists")

            user.change_first_name(cmd.first_name)
            user.change_last_name(cmd.last_name)
            user.change_email(cmd.email)
            user.change_username(cmd.username)

            await self.uow.users.update(user)
            await self.uow.commit()
