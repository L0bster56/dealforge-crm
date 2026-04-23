from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastracture.db.sqlalchemy.funnel.repository import SqlAlchemyFunnelRepository
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.infrastracture.db.sqlalchemy.user.repository import SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.users = SqlAlchemyUserRepository(self.session)
        self.funnels = SqlAlchemyFunnelRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()