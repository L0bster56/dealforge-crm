from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.backend.domain.lead.value_objects.field_type.value_object import FieldType
from src.backend.domain.shared.value_objects.name.value_object import Name


@dataclass
class Lead:
    id: UUID
    name: Name
    is_deleted: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class LeadCustomField:
    id: UUID
    name: Name
    type: FieldType


@dataclass
class LeadCustomFieldEnum:
    id: UUID
    custom_field_id: UUID
    value: str


@dataclass
class LeadCustomFieldValue:
    id: UUID
    custom_field_id: UUID
    lead_id: UUID
    value_text: str | None = None
    value_number: int | None = None
    value_boolean: bool | None = None
    value_date: datetime | None = None
    enum_id: UUID | None = None
