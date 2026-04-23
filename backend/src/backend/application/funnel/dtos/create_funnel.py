from uuid import UUID

from pydantic import BaseModel


class CreateFunnelCommand(BaseModel):
    name: str


class CreateFunnelResult(BaseModel):
    funnel_id: UUID
