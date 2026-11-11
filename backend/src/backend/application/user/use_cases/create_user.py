from dataclasses import dataclass

from src.backend.application.auth.errors import EmailAlreadyExistsError, WeakPasswordError
from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.create_user import CreateUserCommand, CreateUserResult
from src.backend.application.user.errors import UsernameAlreadyExistsError
from src.backend.domain.shared.specification import Specification
from src.backend.domain.user.entity import User
from src.backend.domain.user.policies.can_create import CanCreateUserPolicy


@dataclass
class CreateUserUseCase:
    """
    Use Case создания нового пользователя.

    Отвечает за:
    - проверку прав текущего пользователя (actor)
    - проверку уникальности email и username
    - проверку сложности пароля через Specification
    - создание пользователя через доменную сущность
    - сохранение пользователя в БД через Unit of Work

    Attributes:
        uow: Unit of Work для работы с базой данных.
        hasher: Сервис хеширования паролей.
        actor: Пользователь, выполняющий операцию.
        password_spec: Спецификация проверки сложности пароля.
    """

    uow: UnitOfWork
    hasher: Hasher
    actor: User
    password_spec: Specification[str]

    async def execute(self, cmd: CreateUserCommand) -> CreateUserResult:
        """
        Выполняет создание пользователя.

        Args:
            cmd: Команда создания пользователя.

        Raises:
            PermissionError: если actor не имеет прав (через policy).
            EmailAlreadyExistsError: если email уже существует.
            UsernameAlreadyExistsError: если username уже существует.
            WeakPasswordError: если пароль не проходит проверку сложности.

        Returns:
            CreateUserResult: идентификатор созданного пользователя.
        """
        CanCreateUserPolicy(self.actor, cmd.role).enforce()
        async with self.uow as uow:

            if await self.uow.users.exists_email(cmd.email):
                raise EmailAlreadyExistsError("email already exists")

            if await self.uow.users.exists_username(cmd.username):
                raise UsernameAlreadyExistsError("username already exists")

            if not self.password_spec.is_satisfied_by(cmd.password):
                raise WeakPasswordError("password is too weak")

            user = User.create(
                first_name=cmd.first_name,
                last_name=cmd.last_name,
                username=cmd.username,
                email=cmd.email,
                role=cmd.role,
                password_hash=self.hasher.hash(cmd.password),
            )

            await self.uow.users.create(user)
            await uow.commit()

            return CreateUserResult(user_id=user.id)
