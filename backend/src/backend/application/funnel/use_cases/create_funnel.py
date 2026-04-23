import uuid
from dataclasses import dataclass

from backend.application.funnel.dtos.create_funnel import CreateFunnelResult, CreateFunnelCommand
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.funnel.policies.can_create_funnel import CanCreateFunnelPolicy
from backend.domain.user.entity import User


@dataclass
class CreateFunnelUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: CreateFunnelCommand
    ) -> CreateFunnelResult:
        CanCreateFunnelPolicy(self.user).enforce()

        async with self.uow:
            funnel_id = uuid.uuid4()
            funnel = Funnel.create(
                id=funnel_id,
                name=cmd.name,
            )
            funnel = await self.uow.funnels.create_funnel(funnel)
            return CreateFunnelResult(funnel_id=funnel.id)
