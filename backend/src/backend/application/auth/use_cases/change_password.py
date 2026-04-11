from dataclasses import dataclass
from src.backend.application.auth.dtos.change_password import ChangePasswordCommand
from src.backend.application.auth.errors import (
    AuthUserNotFoundError,
    InvalidPasswordError,
    SamePasswordError,
    WeakPasswordError)
from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.shared.interfaces.uow import UnitOfWork
from tests.unit.domain.shared.specification import Specification


@dataclass
class ChangePasswordUseCase:
    uow: UnitOfWork
    hasher: Hasher
    password_spec : Specification[str]
    password_diff_spec : Specification[tuple[str,str]]

    async def execute(self, cmd: ChangePasswordCommand):
        #Проверка пароля
        if not self.password_spec.is_satisfied_by(cmd.new_password):
            raise WeakPasswordError()

        if not self.password_diff_spec.is_satisfied_by((cmd.old_password, cmd.new_password)):
            raise SamePasswordError()
        async with self.uow as uow:
            user = await uow.find_by_id(cmd.user_id)

            if not user:
                raise AuthUserNotFoundError()

            if not self.hasher.verify(cmd.old_password, user.password_hash):
                raise InvalidPasswordError()

            user.password_hash = self.hasher.hash(cmd.new_password)
            user.change_password(self.hasher.hash(cmd.new_password))
            await self.uow.users.update(user)
            await uow.commit()