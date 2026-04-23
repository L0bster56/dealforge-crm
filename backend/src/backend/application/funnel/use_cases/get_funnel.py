from dataclasses import dataclass

from backend.application.funnel.dtos.get_funnel import GetFunnelCommand
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.user.entity import User


@dataclass
class GetFunnelUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: GetFunnelCommand,
    ) -> Funnel:
        async with self.uow:
            funnel = await self.uow.funnels.get_funnel_by_id(cmd.funnel_id)
            if not funnel:
                raise
            return funnel
