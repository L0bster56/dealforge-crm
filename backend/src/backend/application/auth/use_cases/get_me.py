from dataclasses import dataclass

from src.backend.application.auth.dtos.get_me import GetMeCommand, GetMeResult
from src.backend.application.auth.errors import InActiveUserError
from src.backend.application.auth.interfaces.security.token import TokenService
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User


@dataclass
class GetMeUseCase:
    uow: UnitOfWork
    tokens: TokenService

    async def execute(
            self,
            cmd: GetMeCommand
    ) -> User:
        async with self.uow:
            user_id = self.tokens.decode(cmd.token)

            user = await self.uow.users.get_by_id(user_id)

            if not user:
                raise InActiveUserError("user is not active")

            return user

