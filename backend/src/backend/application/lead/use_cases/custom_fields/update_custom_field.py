from dataclasses import dataclass

from backend.application.lead.dtos.custom_fields.update_custom_field import UpdateCustomFieldCommand
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.lead.entity import LeadCustomField
from backend.domain.lead.policies import CanMangeCustomField
from backend.domain.user.entity import User


@dataclass
class UpdateCustomFieldUseCases:
    uow: UnitOfWork
    user: User
    field: LeadCustomField

    async def execute(
            self,
            cmd: UpdateCustomFieldCommand
    ) -> None:
        CanMangeCustomField(self.user).enforce()
        async with self.uow:
            self.field.rename(cmd.name)

            await self.uow.custom_fields.update(self.field)
            await self.uow.commit()
