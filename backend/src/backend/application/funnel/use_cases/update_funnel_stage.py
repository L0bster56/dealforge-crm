from dataclasses import dataclass

from backend.application.funnel.dtos.update_funnel_stage import UpdateFunnelStageCommand
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel, FunnelStage
from backend.domain.funnel.policies.can_create_funnel import CanCreateFunnelPolicy
from backend.domain.user.entity import User


@dataclass
class UpdateFunnelStageUseCases:
    """
    UseCase обновления стадии воронки.

    Позволяет изменить параметры существующей стадии (название, вероятность, цвет),
    при условии наличия прав у пользователя.

    Attributes:
        uow: Unit of Work для работы с данными.
        funnel: Воронка, к которой относится стадия.
        stage: Стадия, которую необходимо обновить.
        user: Пользователь, выполняющий действие.
    """

    uow: UnitOfWork
    funnel: Funnel
    stage: FunnelStage
    user: User

    async def execute(self, cmd: UpdateFunnelStageCommand):
        """
        Обновляет данные стадии воронки.

        Args:
            cmd: Команда с новыми данными стадии.

        Returns:
            None
        """
        CanCreateFunnelPolicy(self.user).enforce()

        async with self.uow:
            self.stage.change(
                name=cmd.name,
                win_probability=cmd.win_probability,
                hex=cmd.hex,
            )

            await self.uow.stages.update_stage(self.stage)
            await self.uow.commit()