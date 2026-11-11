from src.backend.application.source.dtos.create_source import FormFieldDTO
from src.backend.application.source.dtos.get_source import GetSourceResult, GetSourceConfigDTO, GetWebhookConfigDTO, \
    GetManualConfigDTO, GetPublicFormConfigDTO
from src.backend.domain.source.entity import Source
from src.backend.domain.source.value_objects.source_config.value_object import SourceConfig, WebhookConfig, \
    ManualConfig, PublicFormConfig


def to_result(source: Source) -> GetSourceResult:
    return GetSourceResult(
        id=source.id,
        name=source.name,
        type=source.source_type,
        config=config_to_view(source.config),
        is_active=source.is_active,
        is_deleted=source.is_deleted,
        created_at=source.created_at,
        updated_at=source.updated_at,
    )


def config_to_view(config: SourceConfig) -> GetSourceConfigDTO:
    match config:
        case WebhookConfig():
            return GetWebhookConfigDTO(
                default_funnel_id=config.default_funnel_id,
                default_stage_id=config.default_stage_id,
                assignment_strategy=config.assignment_strategy,
                field_mapping=config.field_mapping,
                assignment_pool=config.assignment_pool,
            )
        case ManualConfig():
            return GetManualConfigDTO()
        case PublicFormConfig():
            return GetPublicFormConfigDTO(
                slug=config.slug,
                fields=[
                    FormFieldDTO(
                        kind=f.kind,
                        label=f.label,
                        is_required=f.is_required,
                        custom_field_id=f.custom_field_id,
                        placeholder=f.placeholder,
                    )
                    for f in config.fields
                ],
                default_funnel_id=config.default_funnel_id,
                default_stage_id=config.default_stage_id,
                assignment_strategy=config.assignment_strategy,
                assignment_pool=config.assignment_pool,
                redirect_url=config.redirect_url,
                success_messages=config.success_messages,
            )
