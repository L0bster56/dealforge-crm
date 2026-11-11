from dataclasses import dataclass
from datetime import date
from uuid import UUID

from backend.domain.lead.value_objects.field_value.error import EmptyFieldValueError, MultipleFieldValueError


@dataclass(frozen=True)
class FieldValue:
    value_text: str | None = None
    value_number: int | None = None
    value_boolean: bool | None = None
    value_date: date | None = None
    enum_id: UUID | None = None

    def __post_init__(self):
        value = [self.value_text, self.value_number, self.value_boolean, self.value_date, self.enum_id]
        value_count = sum(1 for v in value if v is not None)

        if value_count == 0:
            raise EmptyFieldValueError()
        if value_count != 1:
            raise MultipleFieldValueError()
