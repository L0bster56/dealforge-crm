from backend.domain.shared.errors import DomainError


class NotWebhookSourceError(DomainError):
    pass

class SourceConfigTypeMismatch(DomainError):
    pass