from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from backend.application.funnel.use_cases.create_funnel import CreateFunnelUseCase
from backend.application.funnel.use_cases.delete_funnel import DeleteFunnelUseCase
from backend.application.funnel.use_cases.list_funnel import ListFunnelUseCase
from backend.application.funnel.use_cases.update_funnel import UpdateFunnelUseCase
from backend.infrastracture.db.sqlalchemy.funnel.repository.funnel import SqlAlchemyFunnelRepository
from src.backend.application.funnel.dtos.get_funnel import GetFunnelCommand
from src.backend.application.funnel.dtos.get_funnel_stage import GetFunnelStageCommand
from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingServices
from src.backend.application.funnel.use_cases.get_funnel import GetFunnelUseCase
from src.backend.application.funnel.use_cases.get_funnel_stage import GetFunnelStageUseCases
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.user.entity import User
from src.backend.infrastracture.db.sqlalchemy.core.uow import SqlAlchemyUnitOfWork
from src.backend.presentation.api.v1.auth.dependencies import get_current_user, CurrentUserDep
from src.backend.presentation.api.v1.core.dependencies import get_uow, UoWDep, get_db


def get_funnel_repository(
        session: AsyncSession = Depends(get_db),
):
    return SqlAlchemyFunnelRepository(
        session=session
    )


FunnelRepositoryDep = Annotated[
    SqlAlchemyFunnelRepository,
    Depends(get_funnel_repository),
]


async def get_funnel(
        funnel_id: UUID,
        user: User = Depends(get_current_user),
        uow: SqlAlchemyUnitOfWork = Depends(get_uow)
):
    uc = GetFunnelUseCase(
        uow=uow,
        user=user
    )
    funnel = await uc.execute(GetFunnelCommand(funnel_id=funnel_id))
    return funnel


async def get_stage(
        stage_id: UUID,
        funnel: Funnel = Depends(get_funnel),
        uow: SqlAlchemyUnitOfWork = Depends(get_uow)
):
    uc = GetFunnelStageUseCases(
        uow=uow,
        funnel=funnel
    )
    stage = await uc.execute(GetFunnelStageCommand(stage_id=stage_id))
    return stage


def get_ordering() -> FunnelStageOrderingServices:
    return FunnelStageOrderingServices()


def get_create_funnel(
        uow: UoWDep,
        user: CurrentUserDep,
) -> CreateFunnelUseCase:
    return CreateFunnelUseCase(
        uow=uow,
        user=user
    )


GetCreateFunnelDep = Annotated[
    CreateFunnelUseCase,
    Depends(get_create_funnel)
]


def get_funnel_dep(
        funnel_id: UUID,
        repo: FunnelRepositoryDep
) -> Funnel:
    funnel = repo.get_funnel(funnel_id=funnel_id)
    if not funnel:
        raise HTTPException(status_code=404, detail="Funnel not found")
    return funnel

GetFunnelDep = Annotated[
    Funnel,
    Depends(get_funnel_dep),
]

def get_update_funnel(
        uow: UoWDep,
        user: CurrentUserDep,
):
    return UpdateFunnelUseCase(
        uow=uow,
        user=user,
        funnel=GetFunnelDep
    )

UpdateFunnelDep = Annotated[
    UpdateFunnelUseCase,
    Depends(get_update_funnel),
]

def get_delete_funnel(
        uow: UoWDep,
        user: CurrentUserDep,
):
    return DeleteFunnelUseCase(
        uow=uow,
        user=user,
        funnel=GetFunnelDep
    )

DeleteFunnelDep = Annotated[
    DeleteFunnelUseCase,
    Depends(get_delete_funnel),
]

def get_all_funnels(
        uow: UoWDep,
        user: CurrentUserDep,
):
    return ListFunnelUseCase(
        user=user,
        uow=uow,
    )

ListFunnelDep = Annotated[
    ListFunnelUseCase,
    Depends(get_all_funnels),
]
