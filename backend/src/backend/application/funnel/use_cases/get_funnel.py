from dataclasses import dataclass

from backend.application.funnel.dtos.get_funnel import GetFunnelCommand
from backend.application.funnel.error import FunnelNotFoundError
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.user.entity import User


@dataclass
class GetFunnelUseCase:
    """
    UseCase получения воронки по ID.

    Загружает воронку из базы данных через Unit of Work.

    Attributes:
        uow: Unit of Work для доступа к хранилищу данных.
        user: Пользователь, выполняющий запрос (пока не используется в логике).
    """

    uow: UnitOfWork
    user: User

    async def execute(self, cmd: GetFunnelCommand) -> Funnel:
        """
        Получает воронку по её идентификатору.

        Args:
            cmd: Команда, содержащая ID воронки.

        Returns:
            Funnel: Найденная воронка.

        Raises:
            Exception: Если воронка не найдена (лучше заменить на доменную ошибку).
        """
        async with self.uow:
            funnel = await self.uow.funnels.get_funnel_by_id(cmd.funnel_id)

            if not funnel:
                raise FunnelNotFoundError()

            return funnel