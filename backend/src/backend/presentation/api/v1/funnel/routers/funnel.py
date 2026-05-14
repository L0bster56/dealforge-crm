from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from backend.application.funnel.dtos.create_funnel import CreateFunnelResult, CreateFunnelCommand
from backend.application.funnel.dtos.list_funnel import ListFunnelCommand
from backend.application.funnel.dtos.update_funnel import UpdateFunnelCommand
from backend.domain.funnel.entity import Funnel
from backend.domain.user.entity import User
from backend.infrastracture.db.sqlalchemy.core.uow import SqlAlchemyUnitOfWork
from backend.presentation.api.v1.auth.dependencies import get_current_user
from backend.presentation.api.v1.core.dependencies import get_uow
from backend.presentation.api.v1.funnel.dependencies import GetCreateFunnelDep, GetFunnelDep, \
    UpdateFunnelDep, DeleteFunnelDep, ListFunnelDep

router = APIRouter(
    prefix="/funnel",
    tags=["funnel"],
)


@cbv(router)
class FunnelRouter:
    uow: SqlAlchemyUnitOfWork = Depends(get_uow)
    user: User = Depends(get_current_user)

    @router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=CreateFunnelResult,
    )
    async def create_funnel(
            self,
            request: CreateFunnelCommand,
            uc: GetCreateFunnelDep
    ):
        result = uc.execute(request)
        return result

    @router.get(
        "/{funnel_id}",
        response_model=Funnel,
    )
    async def get_funnel(
            self,
            funnel_id: int,
            uc: GetFunnelDep
    ):
        funnel = uc.execute(funnel_id)
        return funnel

    @router.patch(
        "/{funnel_id}",
        status_code=status.HTTP_200_OK,
    )
    async def update_funnel(
            self,
            request: UpdateFunnelCommand,
            uc: UpdateFunnelDep

    ):
        await uc.execute(cmd=request)

    @router.delete(
        "/{funnel_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_funnel(
            self,
            uc: DeleteFunnelDep
    ):
        await uc.execute()

    @router.get(
        "/",
        status_code=status.HTTP_200_OK,
    )
    async def get_all_funnels(
            self,
            cmd: ListFunnelCommand,
            uc: ListFunnelDep
    ):
        result = await uc.execute(cmd=cmd)
        return result
