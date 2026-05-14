from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query

from backend.application.shared.dtos.pagination import PageRequest
from backend.application.source.dtos.create_source import CreateSourceCommand
from backend.application.source.dtos.get_source import GetSourceCommand
from backend.application.source.dtos.list_source import ListSourceCommand, ListSourceSort
from backend.application.source.dtos.update_source import UpdateSourceCommand
from backend.domain.source.enums.source_type.enum import SourceType
from backend.presentation.api.v1.source.dependencies import CreateSourceDep, GetSourceDep, UpdateSourceDep, \
    ActivateSourceDep, DeactivateSourceDep, DeleteSourceDep, RegenerateSourceDep, ListSourceDep

router = APIRouter(
    prefix="/sources",
    tags=["Source"],
)


@router.get(
    "/",
)
async def get_sources(
        uc: ListSourceDep,
        source_type: SourceType | None = Query(None),
        is_active: bool | None = Query(None),
        q: str | None = Query(None),
        sort_by: str | None = Query(None),
        page: int = Query(default=1),
        size: int = Query(default=100),
):
    cmd = ListSourceCommand(
        type=source_type,
        is_active=is_active,
        q=q,
        sort=ListSourceSort(sort_by),
        pagination=PageRequest(page=page, size=size),
    )
    result = await uc.execute(cmd)
    return result


@router.get(
    "/{source_id}"
)
async def get_source(
        source_id: UUID,
        uc: GetSourceDep
):
    result = await uc.execute(
        cmd=GetSourceCommand(source_id=source_id),
    )
    return result


@router.post(
    "/"
)
async def create_source(
        cmd: CreateSourceCommand,
        uc: CreateSourceDep
):
    result = await uc.execute(cmd)
    return result


@router.patch(
    "/{source_id}"
)
async def update_source(
        cmd: UpdateSourceCommand,
        uc: UpdateSourceDep
):
    await uc.execute(cmd)


@router.post(
    "/{source_id}/activate"
)
async def activate_source(
        uc: ActivateSourceDep
):
    await uc.execute()


@router.post(
    "/{source_id}/deactivate"
)
async def deactivate_source(
        uc: DeactivateSourceDep
):
    await uc.execute()


@router.delete(
    "/{source_id}"
)
async def delete_source(
        uc: DeleteSourceDep
):
    await uc.execute()


@router.post(
    "/{source_id}/regenerate"
)
async def regenerate_webhook_secret(
        uc: RegenerateSourceDep
):
    result = await uc.execute()
    return result
