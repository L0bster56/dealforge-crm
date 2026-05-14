from dataclasses import dataclass
from uuid import UUID

from backend.application.funnel.error import StageNotFunnelError
from backend.application.funnel.error import FunnelNotFoundError
from backend.application.lead.error import CustomFieldNotFoundError
from backend.application.shared.interfaces.uow import UnitOfWork
from backend.application.source.error import SlugAlreadyError, AssignmentPoolInvalidRoleError
from backend.domain.source.policies.can_manager import CanManageSourcesPolicy
from src.backend.application.source.dtos.create_source import CreateSourceCommand, CreateSourceResult, \
    CreateWebhookConfigDTO, CreatePublicFormConfigDTO, CreateManualConfigDTO, FormFieldDTO
from backend.domain.source.entity import Source
from backend.domain.source.value_objects.form_field_config.value_object import FormFieldKind, \
    FormFieldConfig
from src.backend.domain.user.entity import User, UserRole


@dataclass
class CreateSourceUseCase:
    uow: UnitOfWork
    user: User
    public_base_url: str = "http://localhost:3000/forms"

    async def execute(
            self,
            cmd: CreateSourceCommand
    ) -> CreateSourceResult:
        CanManageSourcesPolicy(self.user).enforce()
        async with self.uow:
            match cmd.config:
                case CreateWebhookConfigDTO() as cfg:
                    source, token = await self._create_webhook(
                        name=cmd.name,
                        cfg=cfg
                    )
                    result = CreateSourceResult(
                        source_id=source.id,
                        secret_token=token
                    )
                case CreatePublicFormConfigDTO() as cfg:
                    source = await self._create_public_form(
                        name=cmd.name,
                        cfg=cfg
                    )
                    result = CreateSourceResult(
                        source_id=source.id,
                        public_url=self.public_base_url + f"/{cfg.slug}"
                    )
                case CreateManualConfigDTO():
                    source = Source.create_manual(
                        name=cmd.name,
                    )
                    await self.uow.sources.add(source)
                    result = CreateSourceResult(
                        source_id=source.id
                    )
            await self.uow.commit()
        return result

    async def _create_webhook(
            self,
            name: str,
            cfg: CreateWebhookConfigDTO
    ) -> tuple[Source, str]:
        await self._ensure_funnel_and_stage_valid(
            funnel_id=cfg.default_funnel_id,
            stage_id=cfg.default_stage_id
        )
        await self._ensure_assignment_pool(
            assignment_pool=list(cfg.assignment_pool)
        )
        source, token = Source.create_webhook(
            name=name,
            default_funnel_id=cfg.default_funnel_id,
            default_stage_id=cfg.default_stage_id,
            assignment_strategy=cfg.assignment_strategy,
            assignment_pool=cfg.assignment_pool,
            field_mapping=cfg.field_mapping
        )
        await self.uow.sources.add(source)
        return source, token

    async def _create_public_form(
            self,
            name: str,
            cfg: CreatePublicFormConfigDTO
    ):
        await self._ensure_funnel_and_stage_valid(
            funnel_id=cfg.default_funnel_id,
            stage_id=cfg.default_stage_id
        )
        await self._ensure_assignment_pool(
            assignment_pool=list(cfg.assignment_pool)
        )
        await self._ensure_slug_unique(
            slug=cfg.slug
        )
        await self._ensure_custom_field(
            fields=list(cfg.fields)
        )
        domain_fields = tuple(
            FormFieldConfig(
                kind=f.kind,
                label=f.label,
                is_required=f.is_required,
                custom_field_id=f.custom_field_id,
                placeholder=f.placeholder,
            )
            for f in cfg.fields
        )
        source = Source.create_public_form(
            name=name,
            slug=cfg.slug,
            fields=domain_fields,
            default_funnel_id=cfg.default_funnel_id,
            default_stage_id=cfg.default_stage_id,
            assignment_strategy=cfg.assignment_strategy,
            assignment_pool=cfg.assignment_pool,
            redirect_url=cfg.redirect_url,
            success_messages=cfg.success_messages,
        )
        await self.uow.sources.add(source)
        return source

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
