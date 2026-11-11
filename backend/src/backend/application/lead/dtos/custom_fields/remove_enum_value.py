from uuid import UUID

from pydantic import BaseModel


class RemoveEnumValueCommand(BaseModel):
    enum_id: UUID