from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.user.entity import UserRole
from src.backend.domain.user.value_objects.username.value_object import Username


class GetUserByIdCommand(BaseModel):
    user_id: UUID


class GetUserByIdResult(BaseModel):
    first_name: Name
    last_name: Name
    username: Username
    email: Email
    last_interaction: datetime | None
    is_active: bool
    role: UserRole

