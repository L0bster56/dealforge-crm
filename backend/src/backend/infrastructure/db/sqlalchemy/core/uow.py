from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.infrastructure.db.sqlalchemy.user.repository import SqlalchemyUserRepository


class SqlalchemyUnitOfWork(UnitOfWork):
    def __init__(self,session:AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.users = SqlalchemyUserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()