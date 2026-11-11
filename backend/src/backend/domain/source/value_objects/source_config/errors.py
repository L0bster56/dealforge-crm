from backend.domain.shared.errors import DomainError


class EmptyWebhookSecretError(DomainError):
    pass


class InvalidFieldMappingError(DomainError):
    pass


class InvalidSlugError(DomainError):
    pass


class EmptyFormFieldError(DomainError):
    pass


class DuplicateFieldError(DomainError):
    pass
