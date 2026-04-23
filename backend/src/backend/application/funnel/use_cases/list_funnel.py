from dataclasses import dataclass

from backend.application.funnel.dtos.list_funnel import ListFunnelCommand
from backend.application.shared.dtos.pagination import PageResult
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.user.entity import User


@dataclass
class ListFunnelUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: ListFunnelCommand,
    ) -> PageResult[Funnel]:
        async with self.uow:
            result = await self.uow.funnels.get_funnels(cmd=cmd)
            return result