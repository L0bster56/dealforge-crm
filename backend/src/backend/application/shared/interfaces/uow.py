from typing import Protocol

from backend.application.funnel.repository import FunnelRepository, FunnelStageRepository
from backend.application.lead.repository import LeadCustomFieldRepository
from backend.application.source.repository import SourceRepository
from src.backend.application.user.repository import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    funnels: FunnelRepository
    stages: FunnelStageRepository
    custom_fields: LeadCustomFieldRepository
    sources: SourceRepository


    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...