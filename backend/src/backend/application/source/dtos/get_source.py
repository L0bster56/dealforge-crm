from datetime import datetime
from typing import Literal, Annotated, Union
from uuid import UUID

from pydantic import BaseModel, Field

from backend.application.source.dtos.create_source import FormFieldDTO
from backend.domain.source.enums.assignment_strategy.enum import AssignmentStrategyType
from backend.domain.source.enums.source_type.enum import SourceType


class GetSourceCommand(BaseModel):
    source_id: UUID


class GetWebhookConfigDTO(BaseModel):
    type: Literal[SourceType.public_form] = SourceType.webhook
    default_funnel_id: UUID
    default_stage_id: UUID
    assignment_strategy: AssignmentStrategyType = AssignmentStrategyType.manual
    field_mapping: dict[str, str] = Field(default_factory=dict)
    assignment_pool: tuple[UUID, ...] = Field(default_factory=tuple)


class GetPublicFormConfigDTO(BaseModel):
    type: Literal[SourceType.public_form] = SourceType.public_form
    slug: str
    fields: list[FormFieldDTO]
    default_funnel_id: UUID
    default_stage_id: UUID
    assignment_strategy: AssignmentStrategyType = AssignmentStrategyType.manual
    assignment_pool: tuple[UUID, ...] = Field(default_factory=tuple)
    redirect_url: str | None = None
    success_messages: str | None = None


class GetManualConfigDTO(BaseModel):
    type: Literal[SourceType.manual] = SourceType.manual


GetSourceConfigDTO = Annotated[
    Union[GetWebhookConfigDTO, GetPublicFormConfigDTO, GetManualConfigDTO],
    Field(discriminator="type")
]


class GetSourceResult(BaseModel):
    id: UUID
    name: str
    type: SourceType
    config: GetManualConfigDTO
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
