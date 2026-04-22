from uuid import UUID

from pydantic import BaseModel

from src.backend.domain.user.entity import UserRole


class CreateUserCommand(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: UserRole


class CreateUserResult(BaseModel):
    user_id: UUID