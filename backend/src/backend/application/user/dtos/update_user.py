from uuid import UUID

from pydantic import BaseModel


class UpdateUserCommand(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
