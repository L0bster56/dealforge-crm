from uuid import UUID

from pydantic import BaseModel


class GetFunnelCommand(BaseModel):
    funnel_id: UUID
