from dataclasses import dataclass

from backend.application.lead.dtos.custom_fields.get_custom_field import GetCustomFieldCommand
from backend.application.lead.dtos.custom_fields.views import CustomFieldViewDTO
from backend.application.lead.error import CustomFieldNotFoundError
from backend.application.lead.projections.custom_field_view import to_view
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.domain.user.entity import User


@dataclass
class GetCustomFieldUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: GetCustomFieldCommand
    ) -> CustomFieldViewDTO:
        async with self.uow:
            result = await self.uow.custom_fields.get_by_id(cmd.field_id)
            if not result:
                raise CustomFieldNotFoundError()
            if result.is_deleted and not cmd.include_deleted:
                raise CustomFieldNotFoundError()

            return to_view(result)
