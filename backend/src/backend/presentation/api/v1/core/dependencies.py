from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.infrastracture.db.sqlalchemy.core.session import async_session
from src.backend.infrastracture.db.sqlalchemy.core.uow import SqlAlchemyUnitOfWork


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # try:
        async with async_session() as session:
            yield session
    # finally:
    #     await session.close()


async def get_uow(
        session: AsyncSession = Depends(get_db)
) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(
        session=session
    )