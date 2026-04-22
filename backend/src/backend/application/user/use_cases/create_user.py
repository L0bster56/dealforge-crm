import uuid
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
    uow: UnitOfWork
    hasher: Hasher
    actor: User
    password_spec: Specification[str]

    async def execute(
            self,
            cmd: CreateUserCommand
    ):
        async with self.uow:
            CanCreateUserPolicy(self.actor, cmd.role).enforce()

            exists_email = await self.uow.users.exists_email(cmd.email)
            if exists_email:
                raise EmailAlreadyExistsError("email already exists")

            exists_username = await self.uow.users.exists_username(cmd.username)
            if exists_username:
                raise UsernameAlreadyExistsError("username already exists")

            if not self.password_spec.is_satisfied_by(cmd.password):
                raise WeakPasswordError("password is too weak")

            user_id = uuid.uuid4()
            user = User.create(
                id=user_id,
                first_name=cmd.first_name,
                last_name=cmd.last_name,
                username=cmd.username,
                email=cmd.email,
                role=cmd.role,
                password_hash=self.hasher.hash(cmd.password)
            )

            await self.uow.users.create(user)
            await self.uow.commit()

            return CreateUserResult(user_id=user_id)
