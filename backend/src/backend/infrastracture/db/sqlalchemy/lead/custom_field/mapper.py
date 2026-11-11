from backend.domain.lead.entity import LeadCustomField, LeadCustomFieldEnum
from backend.domain.lead.value_objects.field_type.value_object import FieldType
from backend.domain.lead.value_objects.lead_name.value_object import LeadName
from backend.infrastracture.db.sqlalchemy.lead.custom_field.models import LeadCustomFieldModel, LeadCustomFieldEnumModel


def enum_to_model(
        enum: LeadCustomFieldEnum,
) -> LeadCustomFieldEnumModel:
    return LeadCustomFieldEnumModel(
        id=enum.id,
        custom_field_id=enum.custom_field_id,
        value=enum.value,
    )


def enum_to_entity(
        enum: LeadCustomFieldEnumModel,
) -> LeadCustomFieldEnum:
    return LeadCustomFieldEnum(
        id=enum.id,
        custom_field_id=enum.custom_field_id,
        value=enum.value,
    )


def field_to_model(
        entity: LeadCustomField,
) -> LeadCustomFieldModel:
    return LeadCustomFieldModel(
        id=entity.id,
        name=entity.name.value,
        field_type=entity.field_type.value,
        is_deleted=entity.is_deleted,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def field_to_entity(
        model: LeadCustomFieldModel,
        enums: list[LeadCustomFieldEnumModel],
) -> LeadCustomField:
    return LeadCustomField(
        id=model.id,
        name=LeadName(model.name.value),
        field_type=FieldType(model.field_type),
        is_deleted=model.is_deleted,
        enums=[
            enum_to_entity(e)
            for e in enums
        ],
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
