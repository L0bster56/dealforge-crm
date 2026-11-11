from dataclasses import dataclass

from backend.application.funnel.dtos.get_funnel_stage import GetFunnelStageCommand
from backend.application.funnel.use_cases.error import StageNotFunnelError, StageNotFoundError
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel, FunnelStage


@dataclass
class GetFunnelStageUseCases:
    """
    UseCase получения стадии воронки по ID.

    Выполняет загрузку стадии и проверяет, что она принадлежит указанной воронке.

    Attributes:
        uow: Unit of Work для доступа к данным.
        funnel: Воронка, к которой должна принадлежать стадия.
    """

    uow: UnitOfWork
    funnel: Funnel

    async def execute(self, cmd: GetFunnelStageCommand) -> FunnelStage:
        """
        Получает стадию воронки по её идентификатору.

        Args:
            cmd: Команда с ID воронки и стадии.

        Returns:
            FunnelStage: Найденная стадия воронки.

        Raises:
            Exception: Если стадия не найдена или не принадлежит указанной воронке
                      (лучше заменить на доменные ошибки).
        """
        async with self.uow:
            stage = await self.uow.stages.get_funnel_stage_by_id(cmd.stage_id)

            if not stage:
                raise StageNotFoundError()

            if stage.funnel_id != self.funnel.id:
                raise StageNotFunnelError()

            return stage
