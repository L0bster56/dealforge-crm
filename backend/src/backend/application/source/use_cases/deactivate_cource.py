from dataclasses import dataclass

from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.source.entity import Source
from backend.domain.source.policies.can_manager import CanManageSourcesPolicy
from backend.domain.user.entity import User


@dataclass
class DeactivateSourceUseCase:
    uow: UnitOfWork
    source: Source
    user: User


    async def execute(self):
        CanManageSourcesPolicy(self.user).enforce()
        async with self.uow:
            self.source.deactivate()
            await self.uow.sources.update(self.source)
            await self.uow.commit()