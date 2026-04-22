from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.get_user_by_id import GetUserByIdCommand, GetUserByIdResult
from src.backend.application.user.errors import UserNotFoundError


@dataclass
class GetUserByIdUseCase:
    uow: UnitOfWork

    async def execute(
            self,
            cmd: GetUserByIdCommand
    ):
        async with self.uow:
            user = await self.uow.users.get_by_id(cmd.user_id)
            if not user:
                raise UserNotFoundError(f"user with id {cmd.user_id} not found")

            return GetUserByIdResult(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                last_interaction=user.last_interaction,
                is_active=user.is_active,
                role=user.role,
            )
