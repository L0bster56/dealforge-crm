from dataclasses import dataclass

from backend.application.lead.dtos.custom_fields.create_custom_field import CreateCustomFieldCommand, \
    CreateCustomFieldResult
from backend.application.lead.error import CustomFieldNameAlreadyExistsError, SelectFieldWithoutEnumsError
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.lead.entity import LeadCustomField
from backend.domain.lead.policies import CanMangeCustomField

from backend.domain.user.entity import User


@dataclass
class CreateCustomFieldUseCases:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: CreateCustomFieldCommand,
    ):
        CanMangeCustomField(self.user).enforce()
        self._validate_enum_values_match_type(cmd=cmd)
        async with self.uow:
            if await self.uow.custom_fields.name_exists(cmd.name):
                raise CustomFieldNameAlreadyExistsError()
            field = LeadCustomField.create(
                name=cmd.name,
                field_type=cmd.type
            )

            if cmd.type.is_select:
                for value in cmd.values:
                    field.add_enum(value=value)
            await self.uow.custom_fields.add(field)
            await self.uow.commit()

        return CreateCustomFieldResult(field_id=field.id)

    @staticmethod
    def _validate_enum_values_match_type(
            cmd: CreateCustomFieldCommand,
    ):
        if cmd.type.is_select and not cmd.enum_values:
            raise SelectFieldWithoutEnumsError()
        if not cmd.type.is_select and cmd.enum_values:
            raise SelectFieldWithoutEnumsError()
