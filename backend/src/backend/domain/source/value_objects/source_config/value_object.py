import re
from dataclasses import dataclass, field
from typing import Union
from uuid import UUID

from backend.domain.source.enums.assignment_strategy.enum import AssignmentStrategyType
from backend.domain.source.value_objects.form_field_config.value_object import FormFieldConfig
from backend.domain.source.value_objects.source_config.errors import EmptyWebhookSecretError, InvalidFieldMappingError, \
    InvalidSlugError, EmptyFormFieldError, DuplicateFieldError


@dataclass(frozen=True)
class WebhookConfig:
    secret_token_hash: str
    default_funnel_id: UUID
    default_stage_id: UUID
    assignment_strategy: AssignmentStrategyType
    field_mapping: dict[str, str] = field(default_factory=dict)
    assignment_pool: tuple[UUID, ...] = field(default_factory=tuple)

    def ___post_init__(self):
        if not self.secret_token_hash or len(self.secret_token_hash) != 64:
            raise EmptyWebhookSecretError()
        if not isinstance(self.field_mapping, dict):
            raise InvalidFieldMappingError()


@dataclass(frozen=True)
class PublicFormConfig:
    slug: str
    fields: tuple[FormFieldConfig, ...]
    default_funnel_id: UUID
    default_stage_id: UUID
    assignment_strategy: AssignmentStrategyType
    assignment_pool: tuple[UUID, ...] = field(default_factory=tuple)
    redirect_url: str | None = None
    success_messages: str | None = None

    def __post_init__(self):
        if not self.slug or (1 <= len(self.slug) <= 100):
            raise InvalidSlugError()

        if not re.fullmatch(r"[a-z0-9\-]+", self.slug):
            raise InvalidSlugError()

        if len(self.fields) == 0:
            raise EmptyFormFieldError()

        seen_kinds = set()
        for f in self.fields:
            key = (f.kind, f.custom_field_id)
            if key in seen_kinds:
                raise DuplicateFieldError()
            seen_kinds.add(key)


@dataclass(frozen=True)
class ManualConfig:
    pass


SourceConfig = Union[WebhookConfig, PublicFormConfig, ManualConfig]
