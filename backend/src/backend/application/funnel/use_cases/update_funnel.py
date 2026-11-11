from dataclasses import dataclass

from backend.application.funnel.dtos.update_funnel import UpdateFunnelCommand
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.funnel.policies.can_update_funnel import CanUpdateFunnelPolicy
from backend.domain.user.entity import User


@dataclass
class UpdateFunnelUseCase:
    """
    UseCase обновления воронки.

    Позволяет изменить данные существующей воронки (например, название),
    при условии наличия прав у пользователя.

    Attributes:
        uow: Unit of Work для работы с базой данных.
        user: Пользователь, выполняющий действие.
        funnel: Воронка, которую необходимо обновить.
    """

    uow: UnitOfWork
    user: User
    funnel: Funnel

    async def execute(self, cmd: UpdateFunnelCommand) -> None:
        """
        Обновляет данные воронки.

        Args:
            cmd: Команда с новыми данными воронки.

        Returns:
            None
        """
        CanUpdateFunnelPolicy(self.user).enforce()

        async with self.uow:
            self.funnel.change_name(cmd.name)

            await self.uow.funnels.update_funnel(self.funnel)
            await self.uow.commit()