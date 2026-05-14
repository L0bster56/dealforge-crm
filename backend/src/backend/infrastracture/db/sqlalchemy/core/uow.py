from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastracture.db.sqlalchemy.funnel.repository.funnel import SqlAlchemyFunnelRepository
from backend.infrastracture.db.sqlalchemy.funnel.repository.funnel_stage import SqlAlchemyFunnelStageRepository
from backend.infrastracture.db.sqlalchemy.lead.custom_field.repository import SqlAlchemyLeadCustomFieldRepository
from backend.infrastracture.db.sqlalchemy.source.repository import SqlAlchemySourceRepository
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.infrastracture.db.sqlalchemy.user.repository import SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.__commited = False

    async def __aenter__(self):
        self.users = SqlAlchemyUserRepository(self.session)
        self.funnels = SqlAlchemyFunnelRepository(self.session)
        self.stages = SqlAlchemyFunnelStageRepository(self.session)
        self.sources = SqlAlchemySourceRepository(self.session)
        self.custom_fields = SqlAlchemyLeadCustomFieldRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
            return
        if not self.__commited and self.session.in_transaction():
            await self.rollback()

    async def commit(self) -> None:
        await self.session.commit()
        self.__commited = True

    async def rollback(self) -> None:
        await self.session.rollback()
