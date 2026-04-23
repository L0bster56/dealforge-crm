from dataclasses import dataclass

from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.funnel.policies.can_delete_funnel import CanDeleteFunnelPolicy
from backend.domain.user.entity import User


@dataclass
class DeleteFunnelUseCase:
    uow: UnitOfWork
    user: User
    funnel: Funnel

    async def execute(
            self
    ) -> None:
        CanDeleteFunnelPolicy(self.user).enforce()

        async with self.uow:
            self.funnel.delete()

            await self.uow.funnels.delete_funnel(self.funnel)

            await self.uow.commit()
