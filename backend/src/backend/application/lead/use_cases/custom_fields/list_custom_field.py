from dataclasses import dataclass

from backend.application.lead.dtos.custom_fields.list_custom_field import ListCustomFieldCommand
from backend.application.lead.dtos.custom_fields.views import CustomFieldViewDTO
from backend.application.lead.projections.custom_field_view import to_view
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.lead.entity import LeadCustomField
from backend.domain.user.entity import User


@dataclass
class ListCustomFieldUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: ListCustomFieldCommand
    ) -> list[CustomFieldViewDTO]:
        async with self.uow:
            fields = await self.uow.custom_fields.list_all(field_type=cmd.field_type, include_deleted=cmd.include_deleted)
            return [
                to_view(field)
                for field in fields
            ]
