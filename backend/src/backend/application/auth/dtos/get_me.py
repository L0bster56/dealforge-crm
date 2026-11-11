from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.backend.domain.user.entity import UserRole


class GetMeCommand(BaseModel):
    token: str

class GetMeResult(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    role: UserRole
    last_interaction: datetime | None
    is_active: bool

