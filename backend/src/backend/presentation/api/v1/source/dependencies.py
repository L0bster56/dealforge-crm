from typing import Annotated
from uuid import UUID

from fastapi import HTTPException

from backend.application.source.use_cases.activate_source import ActivateSourceUseCase
from backend.application.source.use_cases.create_source import CreateSourceUseCase
from backend.application.source.use_cases.deactivate_cource import DeactivateSourceUseCase
from backend.application.source.use_cases.delete_source import DeleteSourceUseCase
from backend.application.source.use_cases.get_source import GetSourceUseCase
from backend.application.source.use_cases.list_source import ListSourceUseCase
from backend.application.source.use_cases.regenerate_webhook_secret import RegenerateWebhookSecretUseCase
from backend.application.source.use_cases.update_source import UpdateSourceUseCase
from backend.domain.source.entity import Source
from backend.infrastracture.db.sqlalchemy.source.repository import SqlAlchemySourceRepository
from backend.presentation.api.v1.auth.dependencies import CurrentUserDep
from backend.presentation.api.v1.core.dependencies import UoWDep, get_db

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_source_repo(
        session: AsyncSession = Depends(get_db),
) -> SqlAlchemySourceRepository:
    return SqlAlchemySourceRepository(
        session=session,
    )


SourceRepoDep = Annotated[
    SqlAlchemySourceRepository,
    Depends(get_source_repo),
]


def get_create_source_use_cases(
        uow: UoWDep,
        user: CurrentUserDep,
) -> CreateSourceUseCase:
    return CreateSourceUseCase(
        uow=uow,
        user=user,
    )


CreateSourceDep = Annotated[
    CreateSourceUseCase,
    Depends(get_create_source_use_cases),
]


def get_sources_use_cases(
        uow: UoWDep,
        user: CurrentUserDep,
) -> GetSourceUseCase:
    return GetSourceUseCase(
        uow=uow,
        user=user,
    )


GetSourceDep = Annotated[
    GetSourceUseCase,
    Depends(get_sources_use_cases),
]


async def get_current_source(
        source_id: UUID,
        repo: SourceRepoDep
) -> Source:
    source = await repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


CurrentSourceDep = Annotated[
    Source,
    Depends(get_current_source),
]


def get_update_source_use_cases(
        uow: UoWDep,
        user: CurrentUserDep,
        source: CurrentSourceDep
) -> UpdateSourceUseCase:
    return UpdateSourceUseCase(
        uow=uow,
        user=user,
        source=source,
    )


UpdateSourceDep = Annotated[
    UpdateSourceUseCase,
    Depends(get_update_source_use_cases),
]


def get_source_activate_use_cases(
        uow: UoWDep,
        user: CurrentUserDep,
        source: CurrentSourceDep
):
    return ActivateSourceUseCase(
        uow=uow,
        user=user,
        source=source,
    )


ActivateSourceDep = Annotated[
    ActivateSourceUseCase,
    Depends(get_source_activate_use_cases)
]


def get_deactivate_source_use_cases(
        uow: UoWDep,
        user: CurrentUserDep,
        source: CurrentSourceDep
):
    return DeactivateSourceUseCase(
        uow=uow,
        user=user,
        source=source,
    )


DeactivateSourceDep = Annotated[
    DeactivateSourceUseCase,
    Depends(get_deactivate_source_use_cases),
]


def get_delete_source_use_cases(
        uow: UoWDep,
        user: CurrentUserDep,
        source: CurrentSourceDep
):
    return DeleteSourceUseCase(
        uow=uow,
        user=user,
        source=source,
    )


DeleteSourceDep = Annotated[
    DeleteSourceUseCase,
    Depends(get_delete_source_use_cases),
]


def get_regenerate_source_use_cases(
        uow: UoWDep,
        user: CurrentUserDep,
        source: CurrentSourceDep
):
    return RegenerateWebhookSecretUseCase(
        uow=uow,
        user=user,
        source=source,
    )


RegenerateSourceDep = Annotated[
    RegenerateWebhookSecretUseCase,
    Depends(get_regenerate_source_use_cases),
]


def get_lis_source_use_cases(
        uow: UoWDep,
        user: CurrentUserDep,
) -> ListSourceUseCase:
    return ListSourceUseCase(
        uow=uow,
        user=user,
    )

ListSourceDep = Annotated[
    ListSourceUseCase,
    Depends(get_lis_source_use_cases),
]