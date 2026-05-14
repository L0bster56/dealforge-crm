from dataclasses import dataclass

from backend.application.funnel.services.stage_ordering import FunnelStageOrderingServices
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel, FunnelStage
from backend.domain.user.entity import User


@dataclass
class DeleteFunnelStageUseCases:
    """
    UseCase удаления стадии воронки.

    Удаляет стадию и пересчитывает порядок остальных стадий.

    Attributes:
        uow: UnitOfWork.
        funnel: Воронка.
        stage: Стадия, которую нужно удалить.
        ordering: Сервис пересчёта порядка стадий.
        user: Пользователь (сейчас не используется в политике).
    """

    uow: UnitOfWork
    funnel: Funnel
    stage: FunnelStage
    ordering: FunnelStageOrderingServices
    user: User

    async def execute(self) -> None:
        """
        Удаляет стадию воронки и обновляет порядок остальных стадий.

        Returns:
            None
        """
        async with self.uow:
            stages = await self.uow.stages.get_funnel_stages(self.funnel.id)
            updated = self.ordering.remove(stages, self.stage)

            await self.uow.stages.delete_stage(self.stage)
            await self.uow.stages.save_all(updated)
            await self.uow.commit()