from dataclasses import dataclass

from backend.application.funnel.dtos.create_funnel_stage import CreateFunnelStageCommand, CreateFunnelStageResult
from backend.application.funnel.services.stage_ordering import FunnelStageOrderingServices
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel, FunnelStage
from backend.domain.funnel.policies.can_create_funnel import CanCreateFunnelPolicy
from backend.domain.user.entity import User


@dataclass
class CreateFunnelStageUseCase:
    """
    Use Case создания этапа воронки (Funnel Stage).

    Отвечает за:
    - проверку прав пользователя через policy
    - получение существующих этапов воронки
    - создание новой стадии воронки (FunnelStage)
    - вставку стадии в корректную позицию через сервис сортировки
    - сохранение всех стадий в базе данных

    Attributes:
        uow: UnitOfWork для работы с базой данных.
        funnel: воронка, к которой добавляется этап.
        ordering: сервис управления порядком стадий.
        user: пользователь, выполняющий операцию (actor).
    """

    uow: UnitOfWork
    funnel: Funnel
    ordering: FunnelStageOrderingServices
    user: User

    async def execute(self, cmd: CreateFunnelStageCommand) -> CreateFunnelStageResult:
        """
        Выполняет создание нового этапа воронки.

        Args:
            cmd: команда создания этапа воронки.

        Raises:
            PermissionError: если пользователь не имеет прав на создание.

        Returns:
            CreateFunnelStageResult: идентификатор созданного этапа.
        """

        CanCreateFunnelPolicy(self.user).enforce()

        async with self.uow:
            stages = await self.uow.stages.get_funnel_stages(self.funnel.id)

            stage = FunnelStage.create(
                funnel_id=self.funnel.id,
                name=cmd.name,
                win_probability=cmd.win_probability,
                hex_code=cmd.hex,
            )

            position = cmd.position if cmd.position else len(stages)

            updated_stages = self.ordering.insert(
                stages,
                stage,
                position
            )

            await self.uow.stages.save_all(updated_stages)
            await self.uow.commit()

            return CreateFunnelStageResult(
                stage_id=stage.id
            )