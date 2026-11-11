from pydantic import BaseModel


class UpdateFunnelCommand(BaseModel):
    name: str