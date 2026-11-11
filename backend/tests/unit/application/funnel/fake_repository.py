from uuid import UUID

from backend.application.funnel.dtos.list_funnel import ListFunnelCommand
from backend.application.funnel.repository import FunnelRepository
from backend.domain.funnel.entity import Funnel


class FakeRepository(FunnelRepository):
    def __init__(self, funnel: Funnel = None):
        self._funnel = funnel

    async def create_funnel(self, funnel: Funnel):
        return self._funnel

    async def update_funnel(self, funnel: Funnel):
        return self._funnel

    async def delete_funnel(self, funnel: Funnel): pass

    async def  get_funnel_by_id(self, funnel_id: UUID):
        return self._funnel

    async def get_funnels(self, cmd: ListFunnelCommand): pass

