from src.backend.presentation.api.v1.funnel.routers.funnel import router
from src.backend.presentation.api.v1.funnel.routers.funnel_stage import router as funnel_stage_router

router.include_router(funnel_stage_router)
