from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from backend.application.funnel.dtos.get_funnel_stage import GetFunnelStageCommand
from backend.application.funnel.dtos.move_fannel_stage import MoveFunnelStageCommand
from backend.application.funnel.dtos.update_funnel_stage import UpdateFunnelStageCommand
from backend.application.funnel.use_cases.delete_funnel_stage import DeleteFunnelStageUseCases
from backend.application.funnel.use_cases.get_funnel_stage import GetFunnelStageUseCases
from backend.application.funnel.use_cases.move_funnel_stage import MoveFunnelStageUseCases
from backend.application.funnel.use_cases.update_funnel_stage import UpdateFunnelStageUseCases
from src.backend.application.funnel.dtos.create_funnel_stage import CreateFunnelStageResult, CreateFunnelStageCommand
from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingServices
from src.backend.application.funnel.use_cases.create_funnel_stage import CreateFunnelStageUseCase
from src.backend.application.funnel.use_cases.list_funnel_stage import ListFunnelStageUseCase
from src.backend.domain.funnel.entity import Funnel, FunnelStage
from src.backend.domain.user.entity import User
from src.backend.infrastracture.db.sqlalchemy.core.uow import SqlAlchemyUnitOfWork
from src.backend.presentation.api.v1.auth.dependencies import get_current_user
from src.backend.presentation.api.v1.core.dependencies import get_uow
from src.backend.presentation.api.v1.funnel.dependencies import get_funnel, get_ordering, get_stage

router = APIRouter(
    prefix="/{funnel_id}/stages",
    tags=["stages"]
)


@cbv(router)
class FunnelStagesRouter:
    uow: SqlAlchemyUnitOfWork = Depends(get_uow)
    user: User = Depends(get_current_user)
    funnel: Funnel = Depends(get_funnel)

    @router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=CreateFunnelStageResult,
    )
    async def create_funnel_stage(
            self,
            request: CreateFunnelStageCommand,
            ordering: FunnelStageOrderingServices = Depends(get_ordering)
    ):
        uc = CreateFunnelStageUseCase(
            uow=self.uow,
            user=self.user,
            funnel=self.funnel,
            ordering=ordering
        )
        response = await uc.execute(
            cmd=request
        )
        return response

    @router.get(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=Funnel
    )
    async def list_funnel_stages(
            self,
            ordering: FunnelStageOrderingServices = Depends(get_ordering)
    ):
        uc = ListFunnelStageUseCase(
            uow=self.uow,
            funnel=self.funnel,
            ordering=ordering
        )
        response = await uc.execute()
        return response

    @router.get(
        "/{funnel_stage_id}",
        status_code=status.HTTP_200_OK,
    )
    async def get_funnel_stages(
            self,
            cmd: GetFunnelStageCommand
    ):
        uc = GetFunnelStageUseCases(
            uow=self.uow,
            funnel=self.funnel,
        )
        response = await uc.execute(cmd)
        return response

    @router.patch(
        "/{funnel_stage_id}",
        status_code=status.HTTP_200_OK,
    )
    async def update_funnel_stage(
            self,
            cmd: UpdateFunnelStageCommand,
            stage: FunnelStage = Depends(get_stage),
    ):
        uc = UpdateFunnelStageUseCases(
            uow=self.uow,
            funnel=self.funnel,
            stage=stage,
            user=self.user,
        )
        response = await uc.execute(cmd)
        return response

    @router.delete(
        "/{funnel_stage_id}",
        status_code=status.HTTP_204_NO_CONTENT
    )
    async def delete_funnel_stage(
            self,
            stage: FunnelStage = Depends(get_stage),
            ordering: FunnelStageOrderingServices = Depends(get_ordering)
    ):
        uc = DeleteFunnelStageUseCases(
            uow=self.uow,
            user=self.user,
            funnel=self.funnel,
            stage=stage,
            ordering=ordering,
        )
        await uc.execute()

    @router.put(
        "/{funnel_stage}/move",
    )
    async def move_funnel_stage(
            self,
            request: MoveFunnelStageCommand,
            stage: FunnelStage = Depends(get_stage),
            ordering: FunnelStageOrderingServices = Depends(get_ordering)
    ):
        uc = MoveFunnelStageUseCases(
            uow=self.uow,
            funnel=self.funnel,
            stage=stage,
            ordering=ordering,
        )
        await uc.execute(
            cmd=request
        )
