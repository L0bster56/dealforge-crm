from dataclasses import dataclass, replace
from uuid import UUID

from backend.application.funnel.error import StageNotFunnelError, FunnelNotFoundError
from backend.application.lead.error import CustomFieldNotFoundError
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.application.source.dtos.update_source import UpdateWebhookConfigDTO, UpdatePublicFormConfigDTO, \
    UpdateManualConfigDTO, FormFieldDTO, UpdateSourceConfigDTO
from backend.application.source.error import SlugAlreadyError, AssignmentPoolInvalidRoleError, CanNotSourceTypeError
from backend.domain.source.entity import Source
from backend.domain.source.policies.can_manager import CanManageSourcesPolicy
from backend.domain.source.value_objects.form_field_config.value_object import FormFieldConfig, FormFieldKind
from backend.domain.source.value_objects.source_config.value_object import SourceConfig, WebhookConfig, PublicFormConfig
from backend.domain.user.entity import User, UserRole


@dataclass
class UpdateSourceUseCase:
    uow: UnitOfWork
    user: User
    source: Source

    async def execute(
            self,
            cmd
    ) -> None:
        CanManageSourcesPolicy(self.user).enforce()
        async with self.uow:
            if cmd.name is not None:
                self.source.change_name(cmd.name)
            if cmd.config is not None:
                if cmd.config.type != self.source.source_type:
                    raise CanNotSourceTypeError()
                new_config = await self._build_update_config(self.source, cmd.config)
                if new_config is not None:
                    self.source.change_config(new_config)
            await self.uow.sources.update(self.source)
            await self.uow.commit()

    async def _build_update_config(
            self,
            source: Source,
            patch: UpdateSourceConfigDTO
    ) -> SourceConfig | None:
        match patch:
            case UpdateWebhookConfigDTO():
                config = await self._update_webhook_config(source.config, patch)
                return config
            case UpdatePublicFormConfigDTO():
                config = await self._update_public_form(source, patch)
                return config
            case UpdateManualConfigDTO():
                return None

    async def _update_webhook_config(
            self,
            current: WebhookConfig,
            patch: UpdateWebhookConfigDTO
    ) -> WebhookConfig:
        change = patch.model_dump(exclude_unset=True, exclude={"type"})
        if not change:
            return current
        new_funnel_id = change.get("default_funnel_id", current.default_funnel_id)
        new_stage_id = change.get("default_stage_id", current.default_stage_id)
        if "default_funnel_id" in change or "default_stage_id" in change:
            await self._ensure_funnel_and_stage_valid(new_funnel_id, new_stage_id)
        if "assignment_pool" in change:
            await self._ensure_assignment_pool(change["assignment_pool"])
            change["assignment_pool"] = tuple(change["assignment_pool"])
        return replace(current, **change)

    async def _update_public_form(
            self,
            source: Source,
            patch: UpdatePublicFormConfigDTO
    ):
        current: PublicFormConfig = source.config
        change = patch.model_dump(exclude_unset=True, exclude={"type"})
        if not change:
            return current

        if "slug" in change and change["slug"] != current.slug:
            await self._ensure_slug_unique(change["slug"])

        new_funnel_id = change.get("default_funnel_id", current.default_funnel_id)
        new_stage_id = change.get("default_stage_id", current.default_stage_id)

        if "default_funnel_id" in change or "default_stage_id" in change:
            await self._ensure_funnel_and_stage_valid(new_funnel_id, new_stage_id)

        if "assignment_pool" in change:
            await self._ensure_assignment_pool(change["assignment_pool"])
            change["assignment_pool"] = tuple(change["assignment_pool"])

        if "fields" in change:
            new_fields = patch.fields
            await self._ensure_custom_field(list(new_fields))
            change["fields"] = tuple(
                FormFieldConfig(
                    kind=f.kind,
                    label=f.label,
                    is_required=f.is_required,
                    custom_field_id=f.custom_field_id,
                    placeholder=f.placeholder,
                )
                for f in new_fields
            )
        return replace(current, **change)

    async def _ensure_funnel_and_stage_valid(
            self,
            funnel_id: UUID,
            stage_id: UUID,
    ):
        funnel = await self.uow.funnels.get_funnel_by_id(funnel_id)
        if not funnel or funnel.is_deleted:
            raise FunnelNotFoundError()

        stage = await self.uow.stages.get_funnel_stage_by_id(stage_id)
        if not stage:
            raise StageNotFunnelError()

        if stage.funnel_id != funnel_id:
            raise StageNotFunnelError()

    async def _ensure_assignment_pool(
            self,
            assignment_pool: list[UUID]
    ):
        if len(assignment_pool) == 0:
            return

        users = await self.uow.users.list_by_ids(assignment_pool)
        existing_ids = {u.id for u in users}

        for uid in existing_ids:
            if uid not in assignment_pool:
                raise AssignmentPoolInvalidRoleError()

        for u in users:
            if not u.is_active:
                raise AssignmentPoolInvalidRoleError()

            if u.role not in [UserRole.sales_manager, UserRole.consultant]:
                raise AssignmentPoolInvalidRoleError()

    async def _ensure_slug_unique(
            self,
            slug: str
    ):
        exists = await self.uow.sources.exists_slug(slug)
        if exists:
            raise SlugAlreadyError()

    async def _ensure_custom_field(
            self,
            fields: list[FormFieldDTO]
    ):
        custom_field_ids = [
            f.custom_field_id
            for f in fields
            if f.kind == FormFieldKind.custom_field and f.custom_field_id
        ]
        if not custom_field_ids:
            return

        existing = await self.uow.custom_fields.list_by_ids(custom_field_ids)
        existing_ids = {cf.id for cf in existing if not cf.is_deleted}

        for cf_id in custom_field_ids:
            if cf_id not in existing_ids:
                raise CustomFieldNotFoundError()
