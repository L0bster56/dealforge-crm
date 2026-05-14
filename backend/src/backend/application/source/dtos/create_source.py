from typing import Literal, Annotated, Union
from uuid import UUID

from pydantic import BaseModel, Field

from backend.domain.source.enums.assignment_strategy.enum import AssignmentStrategyType
from backend.domain.source.enums.source_type.enum import SourceType
from backend.domain.source.value_objects.form_field_config.value_object import FormFieldKind


class FormFieldDTO(BaseModel):
    kind: FormFieldKind
    label: str
    is_required: bool = False
    custom_field_id: UUID | None = None
    placeholder: str | None = None


class CreateWebhookConfigDTO(BaseModel):
    type: Literal[SourceType.public_form] = SourceType.webhook
    default_funnel_id: UUID
    default_stage_id: UUID
    assignment_strategy: AssignmentStrategyType = AssignmentStrategyType.manual
    field_mapping: dict[str, str] = Field(default_factory=dict)
    assignment_pool: tuple[UUID, ...] = Field(default_factory=tuple)


class CreatePublicFormConfigDTO(BaseModel):
    type: Literal[SourceType.public_form] = SourceType.public_form
    slug: str
    fields: tuple[FormFieldDTO, ...]
    default_funnel_id: UUID
    default_stage_id: UUID
    assignment_strategy: AssignmentStrategyType = AssignmentStrategyType.manual
    assignment_pool: tuple[UUID, ...] = Field(default_factory=tuple)
    redirect_url: str | None = None
    success_messages: str | None = None


class CreateManualConfigDTO(BaseModel):
    type: Literal[SourceType.manual] = SourceType.manual


CreateSourceConfigDTO = Annotated[
    Union[CreateWebhookConfigDTO, CreatePublicFormConfigDTO, CreateManualConfigDTO],
    Field(discriminator="type")
]


class CreateSourceCommand(BaseModel):
    name: str
    config: CreateSourceConfigDTO


class CreateSourceResult(BaseModel):
    source_id: UUID

    secret_token: str | None = None
    public_url: str | None = None
