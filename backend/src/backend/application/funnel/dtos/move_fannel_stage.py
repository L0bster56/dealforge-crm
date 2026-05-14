from pydantic import BaseModel


class MoveFunnelStageCommand(BaseModel):
    position: int