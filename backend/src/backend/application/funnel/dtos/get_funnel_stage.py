from uuid import UUID

from pydantic import BaseModel


class GetFunnelStageCommand(BaseModel):
    stage_id: UUID