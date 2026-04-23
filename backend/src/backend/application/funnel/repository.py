from typing import Protocol, List
from uuid import UUID

from backend.application.funnel.dtos.list_funnel import ListFunnelCommand
from backend.application.shared.dtos.pagination import PageResult
from backend.domain.funnel.entity import Funnel


class FunnelRepository(Protocol):
    async def create_funnel(self, funnel: Funnel) -> Funnel: ...

    async def update_funnel(self, funnel: Funnel) -> Funnel: ...

    async def delete_funnel(self, funnel: Funnel) -> None: ...

    async def get_funnel_by_id(self, funnel_id: UUID) -> Funnel | None: ...

    async def get_funnels(self, cmd: ListFunnelCommand) -> PageResult[Funnel] | None: ...
