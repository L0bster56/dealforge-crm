from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID

from backend.domain.source.value_objects.form_field_config.error import InvalidFormFieldLabelError, \
    CustomFieldKindRequiresError, FieldIdNotAllowedError


class FormFieldKind(StrEnum):
    fullname = "fullname"
    email = "email"
    phone = "phone"
    telegram = "telegram"
    custom_field = "custom_field"


@dataclass(frozen=True)
class FormFieldConfig:
    kind: FormFieldKind
    label: str
    is_required: bool = field(default=False)
    custom_field_id: UUID | None = field(default=None)
    placeholder: str | None = field(default=None)

    def __post_init__(self):
        if not self.label or len(self.label) > 100:
            raise InvalidFormFieldLabelError()

        if self.kind == FormFieldKind.custom_field and self.custom_field_id is None:
            raise CustomFieldKindRequiresError()

        if self.kind != FormFieldKind.custom_field and self.custom_field_id is not None:
            raise FieldIdNotAllowedError()
