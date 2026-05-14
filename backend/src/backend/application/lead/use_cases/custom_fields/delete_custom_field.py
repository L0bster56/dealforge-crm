from dataclasses import dataclass

from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.lead.entity import LeadCustomField
from backend.domain.lead.policies import CanMangeCustomField
from backend.domain.user.entity import User


@dataclass
class DeleteCustomFieldUseCase:
    uow: UnitOfWork
    user: User
    field: LeadCustomField

    async def execute(
            self
    ) -> None:
        CanMangeCustomField(self.user).enforce()
        async with self.uow:
            self.field.delete()
            await self.uow.custom_fields.update(field=self.field)
            await self.uow.commit()