from dataclasses import dataclass

from backend.application.funnel.dtos.list_funnel import ListFunnelCommand
from backend.application.shared.dtos.pagination import PageResult
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.user.entity import User


@dataclass
class ListFunnelUseCase:
    """
    UseCase получения списка воронок.

    Выполняет выборку воронок с поддержкой фильтрации и пагинации.

    Attributes:
        uow: Unit of Work для доступа к данным.
        user: Пользователь, выполняющий запрос (пока не используется в логике).
    """

    uow: UnitOfWork
    user: User

    async def execute(self, cmd: ListFunnelCommand) -> PageResult[Funnel]:
        """
        Получает список воронок с пагинацией и фильтрацией.

        Args:
            cmd: Команда с параметрами фильтрации и пагинации.

        Returns:
            PageResult[Funnel]: Страница с воронками.
        """
        async with self.uow:
            result = await self.uow.funnels.get_funnels(cmd=cmd)
            return result