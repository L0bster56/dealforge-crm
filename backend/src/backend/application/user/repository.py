#repository.py
from typing import Protocol
from uuid import UUID

from src.backend.domain.user.entity import User


class UserRepository(Protocol):
    """
    Interface для User Repository
    """

    async def get_by_username(self, username: str) -> User: ...

    async def get_by_email(self, email: str) -> User: ...

    async def get_by_id(self, user_id: UUID) -> User: ...

    async def create(self, user: User) -> User: ...

    async def update(self, user: User) -> None: ...

    async def delete(self, user: User) -> None: ...

    async def list(self): ...