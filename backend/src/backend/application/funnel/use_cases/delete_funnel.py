from dataclasses import dataclass

from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.funnel.entity import Funnel
from backend.domain.funnel.policies.can_delete_funnel import CanDeleteFunnelPolicy
from backend.domain.user.entity import User


@dataclass
class DeleteFunnelUseCase:
    """
    Use Case удаления воронки (Funnel).

    Отвечает за:
    - проверку прав пользователя через policy
    - изменение состояния доменной сущности (soft delete)
    - удаление воронки через репозиторий
    - фиксацию изменений в базе данных

    Attributes:
        uow: UnitOfWork для работы с базой данных.
        user: пользователь, выполняющий операцию (actor).
        funnel: воронка, которую необходимо удалить.
    """

    uow: UnitOfWork
    user: User
    funnel: Funnel

    async def execute(self) -> None:
        """
        Выполняет удаление воронки.

        Raises:
            PermissionError: если пользователь не имеет прав на удаление.

        Returns:
            None
        """

        CanDeleteFunnelPolicy(self.user).enforce()

        async with self.uow:
            self.funnel.delete()

            await self.uow.funnels.update_funnel(self.funnel)

            await self.uow.commit()
