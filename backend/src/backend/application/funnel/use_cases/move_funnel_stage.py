from dataclasses import dataclass

from backend.application.funnel.dtos.move_fannel_stage import MoveFunnelStageCommand
from backend.application.funnel.services.stage_ordering import FunnelStageOrderingServices
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel, FunnelStage


@dataclass
class MoveFunnelStageUseCases:
    """
    UseCase перемещения стадии воронки.

    Переставляет стадию в указанную позицию и пересчитывает порядок остальных стадий.

    Attributes:
        uow: Unit of Work для работы с хранилищем данных.
        funnel: Воронка, к которой относится стадия.
        stage: Стадия, которую необходимо переместить.
        ordering: Сервис управления порядком стадий.
    """

    uow: UnitOfWork
    funnel: Funnel
    stage: FunnelStage
    ordering: FunnelStageOrderingServices

    async def execute(self, cmd: MoveFunnelStageCommand):
        """
        Перемещает стадию воронки на новую позицию.

        Args:
            cmd: Команда, содержащая новую позицию стадии.

        Returns:
            None
        """
        async with self.uow:
            stages = await self.uow.stages.get_funnel_stages(self.funnel.id)
            updated = self.ordering.move(stages, self.stage, cmd.position)

            await self.uow.stages.save_all(updated)
            await self.uow.commit()