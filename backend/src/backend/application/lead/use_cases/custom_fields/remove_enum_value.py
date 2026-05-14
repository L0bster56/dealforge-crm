from dataclasses import dataclass

from backend.application.lead.dtos.custom_fields.remove_enum_value import RemoveEnumValueCommand
from backend.application.lead.error import EnumInUseError
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.lead.entity import LeadCustomField
from backend.domain.lead.policies import CanMangeCustomField
from backend.domain.lead.value_objects.lead_name.value_object import LeadName
from backend.domain.user.entity import User


@dataclass
class RemoveEnumValueUseCase:
    uow: UnitOfWork
    user: User
    custom_field: LeadCustomField

    async def execute(
            self,
            cmd: RemoveEnumValueCommand
    )-> None:
        CanMangeCustomField(self.user).enforce()
        async with self.uow:
            usage_count = await self.uow.custom_fields.count_values_with_enum_values(cmd.enum_id)

            if usage_count > 0:
                raise EnumInUseError()

            self.custom_field.remove(cmd.enum_id)
            await self.uow.custom_fields.update(self.custom_field)
            await self.uow.commit()

