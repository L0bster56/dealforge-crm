from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User
from tests.unit.application.user.fake_repository import FakeUserRepository


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, user: User = None):
        self._user = user

    async def __aenter__(self):
        self.users = FakeUserRepository(self._user)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
