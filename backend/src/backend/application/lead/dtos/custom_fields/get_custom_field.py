from uuid import UUID

from pydantic import BaseModel


class GetCustomFieldCommand(BaseModel):
    field_id: UUID
    include_deleted: bool
