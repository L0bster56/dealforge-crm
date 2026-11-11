from dataclasses import dataclass

from backend.application.shared.dtos.pagination import PageResult
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.application.source.dtos.get_source import GetSourceResult
from backend.application.source.dtos.list_source import ListSourceCommand
from backend.application.source.source_view import to_result
from backend.domain.user.entity import User


@dataclass
class ListSourceUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: ListSourceCommand,
    ):
        async with self.uow:
            sources = await self.uow.sources.list(cmd)

            return PageResult[GetSourceResult](
                items=[
                    to_result(sources)
                    for sources in sources.items
                ],
                page=sources.page,
                size=sources.size,
                total_items=sources.total_items,
            )

