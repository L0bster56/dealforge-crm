from dataclasses import dataclass

from backend.application.funnel.services.stage_ordering import FunnelStageOrderingServices
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel


@dataclass
class ListFunnelStageUseCase:
    """
    UseCase получения списка стадий воронки.

    Загружает стадии воронки и приводит их к нормальному (упорядоченному) виду
    через сервис сортировки/нормализации.

    Attributes:
        uow: Unit of Work для доступа к данным.
        funnel: Воронка, для которой загружаются стадии.
        ordering: Сервис управления порядком стадий.
    """

    uow: UnitOfWork
    funnel: Funnel
    ordering: FunnelStageOrderingServices

    async def execute(self):
        """
        Получает список стадий воронки.

        Returns:
            list[FunnelStage]: Отсортированные и нормализованные стадии.
        """
        async with self.uow:
            stages = await self.uow.stages.get_funnel_stages(self.funnel.id)
            return self.ordering.normalize(stages)