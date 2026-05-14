from uuid import UUID

from mypy.semanal_shared import Protocol

from backend.application.shared.dtos.pagination import PageResult
from backend.application.source.dtos.list_source import ListSourceCommand
from backend.domain.source.entity import Source


class SourceRepository(Protocol):
    async def add(self, source: Source) -> Source: ...

    async def update(self, source: Source) -> Source: ...

    async def exists_slug(self, slug: str) -> bool: ...

    async def get_by_id(self, source_id: UUID) -> Source: ...

    async def list(self, cmd: ListSourceCommand) -> PageResult[Source]: ...


