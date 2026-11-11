from uuid import UUID

from pydantic import BaseModel

from backend.domain.lead.value_objects.field_type.value_object import FieldType


class CreateCustomFieldCommand(BaseModel):
    name: str
    type: FieldType
    enum_values: list[str]

class CreateCustomFieldResult(BaseModel):
    field_id: UUID