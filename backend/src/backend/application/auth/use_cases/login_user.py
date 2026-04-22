from src.backend.application.auth.dtos.login_user import LoginUserCommand, LoginUserResult
from src.backend.application.auth.errors import AuthUserNotFoundError, InvalidPasswordError, InActiveUserError
from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.auth.interfaces.security.token import TokenService
from src.backend.application.shared.interfaces.uow import UnitOfWork


class LoginUserUseCase:
    def __init__(
            self,
            uow: UnitOfWork,
            tokens: TokenService,
            hasher: Hasher
    ):
        self.uow = uow
        self.tokens = tokens
        self.hasher = hasher

    async def execute(
            self,
            cmd: LoginUserCommand
    ):
        async with self.uow:
            user = await self.uow.users.get_by_username(cmd.username)

            if not user:
                raise AuthUserNotFoundError("invalid password or username")

            if not self.hasher.verify(cmd.password, user.password_hash):
                raise InvalidPasswordError("invalid password or username")

            if not user.is_active:
                raise InActiveUserError("user is not active")

            access_token = self.tokens.encode(user.id)
            refresh_token = self.tokens.encode(user.id,  True)
            token_type = self.tokens.get_token_type()

            return LoginUserResult(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=token_type
            )