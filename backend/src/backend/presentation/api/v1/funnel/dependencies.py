from typing import Any, Coroutine
from uuid import UUID

from fastapi.params import Depends

from backend.application.funnel.dtos.get_funnel import GetFunnelCommand
from backend.application.funnel.use_cases.get_funnel import GetFunnelUseCase
from backend.domain.funnel.entity import Funnel
from backend.domain.user.entity import User
from backend.infrastracture.db.sqlalchemy.core.uow import SqlAlchemyUnitOfWork
from backend.presentation.api.v1.auth.dependencies import get_current_user
from backend.presentation.api.v1.core.dependencies import get_uow


async def get_funnel(
        funnel_id: UUID,
        user: User = Depends(get_current_user),
        uow: SqlAlchemyUnitOfWork = Depends(get_uow)
) -> Coroutine[Any, Any, Funnel]:
    uc = GetFunnelUseCase(
        uow=uow,user=user,
    )
    funnel = uc.execute(GetFunnelCommand(funnel_id=funnel_id))
    return funnel

