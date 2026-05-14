from dataclasses import dataclass, field
from uuid import UUID

from backend.domain.lead.error import FieldTypeNotSelectError, EnumValueAlreadyExistsError, InvalidEnumIdError
from backend.domain.lead.value_objects.contact.value_object import Contact
from backend.domain.lead.value_objects.field_value.value_object import FieldValue
from backend.domain.lead.value_objects.lead_name.value_object import LeadName
from backend.domain.shared.entity import BaseEntity
from backend.domain.shared.mixins import TimeActionMixin

from src.backend.domain.lead.value_objects.field_type.value_object import FieldType


@dataclass
class LeadCustomFieldEnum(BaseEntity):
    custom_field_id: UUID
    value: str

    @classmethod
    def create(
            cls,
            custom_field_id: UUID,
            value: str,
    ):
        return cls(
            custom_field_id=custom_field_id,
            value=value,
        )


@dataclass
class LeadCustomField(BaseEntity, TimeActionMixin):
    name: LeadName
    field_type: FieldType
    enums: list[LeadCustomFieldEnum] = field(default_factory=list)
    is_deleted: bool = field(default=False)

    @classmethod
    def create(
            cls,
            name: str,
            field_type: FieldType,

    ):
        return cls(
            name=LeadName(name),
            field_type=field_type,
        )

    def delete(self):
        self.is_deleted = True
        self._touch()

    def restore(self) -> None:
        self.is_deleted = False
        self._touch()


    def add_enum(
            self,
            value: str
    ):
        if self.field_type.is_select:
            raise FieldTypeNotSelectError()
        if any(e.value == value for e in self.enums):
            raise EnumValueAlreadyExistsError()

        new_enum = LeadCustomFieldEnum.create(self.id, value)
        self.enums.append(new_enum)
        self._touch()

    def remove(self, enum_id: UUID):
        self.enums = [e for e in self.enums if e.id == enum_id]
        self._touch()

    def rename(self, new_name: str):
        self.name = LeadName(new_name)
        self._touch()


@dataclass
class LeadCustomFieldValue(BaseEntity):
    custom_field_id: UUID
    lead_id: UUID
    value: FieldValue

    @classmethod
    def create(
            cls,
            custom_field_id: UUID,
            lead_id: UUID,
            value: FieldValue,
    ):
        return cls(
            custom_field_id=custom_field_id,
            lead_id=lead_id,
            value=value,
        )


@dataclass
class Lead(BaseEntity, TimeActionMixin):
    """
    Представляет лида.

    Attributes:
        name: имя лида
        contact: контактная информация
        is_delete: флаг удаления
        assign_to: назначенный пользователь
        custom_values: LeadCustomFieldValue — список кастомных значений
    """
    name: LeadName
    contact: Contact
    source_id: UUID
    stage_id: UUID
    is_delete: bool = field(default=False)
    assign_to: UUID | None = None
    funnel_id: UUID | None = None
    custom_values: list[LeadCustomFieldValue] = field(default_factory=list)

    def set_custom_value(
            self,
            custom_field: LeadCustomField,
            value: FieldValue
    ):
        custom_field.field_type.validate_value(value)

        if value.enum_id is not None:
            valid_enum_ids = {e.id for e in custom_field.enums}
            if value.enum_id not in valid_enum_ids:
                raise InvalidEnumIdError()

        if custom_field.field_type.is_multi:
            self._add_multi_value(custom_field.id, value)
        else:
            self._add_single_value(custom_field.id, value)

        self._touch()

    def _add_multi_value(
            self,
            custom_field_id: UUID,
            value: FieldValue
    ) -> None:
        existing = self._find_value(custom_field_id, value.enum_id)
        if existing is not None:
            return
        self.custom_values.append(
            LeadCustomFieldValue.create(
                custom_field_id=custom_field_id,
                value=value,
                lead_id=self.id
            )
        )

    def _add_single_value(
            self,
            custom_field_id: UUID,
            value: FieldValue
    ) -> None:
        existing = self._find_value(custom_field_id)
        if existing is not None:
            existing.value = value
            return
        self.custom_values.append(
            LeadCustomFieldValue.create(
                custom_field_id=custom_field_id,
                value=value,
                lead_id=self.id
            )
        )

    def remove_custom_value(
            self,
            custom_field_value_id: UUID
    ):
        self.custom_values = [
            v for v in self.custom_values if v.id != custom_field_value_id
        ]
        self._touch()

    def _find_value(
            self,
            custom_field_id: UUID,
            enum_id: UUID | None = None
    ) -> LeadCustomFieldValue | None:
        option = lambda v: (
            v for v in self.custom_values if v.custom_field_id == custom_field_id and v.value.enum_id == enum_id
        ) if enum_id is not None else (
                v.custom_field_id == custom_field_id
        )
        return next(
            (v for v in self.custom_values if option(v)),
            None
        )

    def delete(self):
        self.is_delete = True
        self._touch()
