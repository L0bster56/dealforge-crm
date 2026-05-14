from enum import StrEnum

from backend.domain.lead.value_objects.field_value.value_object import FieldValue


class FieldType(StrEnum):
    text = "text"
    number = "number"
    date = "date"
    select_one = "select_one"
    select_many = "select_many"
    boolean = "boolean"

    @property
    def is_multi(self) -> bool:
        return self == FieldType.select_many

    @property
    def is_select(self) -> bool:
        return self in (FieldType.select_one, FieldType.select_many)

    def validate_value(self, value: "FieldValue") -> None:
        match self:
            case FieldType.text:
                if value.value_text is None:
                    raise ValueError()
            case FieldType.number:
                if value.value_number is None:
                    raise ValueError()
            case FieldType.date:
                if value.value_date is None:
                    raise
            case FieldType.boolean:
                if value.value_boolean is None:
                    raise ValueError()
            case FieldType.select_one:
                if value.enum_id is None:
                    raise ValueError()
