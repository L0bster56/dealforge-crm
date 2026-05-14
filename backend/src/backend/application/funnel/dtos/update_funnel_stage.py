from pydantic import BaseModel


class UpdateFunnelStageCommand(BaseModel):
    name: str
    win_probability: int
    hex: str
