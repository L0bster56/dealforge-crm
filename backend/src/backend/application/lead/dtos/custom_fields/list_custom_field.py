from pydantic import BaseModel

from backend.domain.lead.value_objects.field_type.value_object import FieldType


class ListCustomFieldCommand(BaseModel):
    type: FieldType | None = None
    include_deleted: bool | None = None
