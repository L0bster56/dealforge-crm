from dataclasses import dataclass

from backend.application.shared.interfaces.uow import UnitOfWork
from backend.application.source.dtos.get_source import GetSourceCommand, GetSourceResult
from backend.application.source.error import SourceNotFoundError
from backend.application.source.source_view import to_result

from backend.domain.user.entity import User


@dataclass
class GetSourceUseCase:
    uow: UnitOfWork
    user: User
    public_base_url: str = "http://localhost:3000/forms"

    async def execute(
            self,
            cmd: GetSourceCommand,
    ) -> GetSourceResult:
        async with self.uow:
            source = await self.uow.sources.get_by_id(cmd.source_id)
            if not source or source.is_deleted:
                raise SourceNotFoundError()

            return to_result(source)
