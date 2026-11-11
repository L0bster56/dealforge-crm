from dataclasses import dataclass

from backend.application.funnel.dtos.create_funnel import CreateFunnelResult, CreateFunnelCommand
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.funnel.policies.can_create_funnel import CanCreateFunnelPolicy
from backend.domain.user.entity import User


@dataclass
class CreateFunnelUseCase:
    """
    Use Case создания воронки (Funnel).

    Отвечает за:
    - проверку прав пользователя через policy
    - создание доменной сущности Funnel
    - сохранение воронки в базе данных через UnitOfWork

    Attributes:
        uow: UnitOfWork для работы с базой данных.
        user: пользователь, выполняющий операцию (actor).
    """

    uow: UnitOfWork
    user: User

    async def execute(self, cmd: CreateFunnelCommand) -> CreateFunnelResult:
        """
        Выполняет создание новой воронки.

        Args:
            cmd: команда создания воронки.

        Raises:
            PermissionError: если пользователь не имеет прав на создание воронки.

        Returns:
            CreateFunnelResult: идентификатор созданной воронки.
        """

        CanCreateFunnelPolicy(self.user).enforce()

        async with self.uow:
            funnel = Funnel.create(
                name=cmd.name,
            )

            funnel = await self.uow.funnels.create_funnel(funnel)
            await self.uow.commit()

            return CreateFunnelResult(
                funnel_id=funnel.id
            )