from dataclasses import dataclass

from backend.application.lead.dtos.custom_fields.add_enum_value import AddEnumValueCommand
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.lead.entity import LeadCustomField
from backend.domain.lead.policies import CanMangeCustomField
from backend.domain.user.entity import User


@dataclass
class AddEnumValueUseCases:
    uow: UnitOfWork
    user: User
    custom_field: LeadCustomField

    async def execute(
            self,
            cmd: AddEnumValueCommand,
    ) -> None:
        CanMangeCustomField(self.user).enforce()
        async with self.uow:
            self.custom_field.add_enum(cmd.value)
            await self.uow.custom_fields.update(self.custom_field)
            await self.uow.commit()