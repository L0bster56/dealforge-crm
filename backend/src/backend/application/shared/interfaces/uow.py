from typing import Protocol

from src.backend.application.user.repository import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...