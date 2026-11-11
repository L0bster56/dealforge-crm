from backend.domain.shared.errors import DomainError


class SourceConfigTypeMismatch(DomainError):
    pass

class NotWebhookSourceError(DomainError):
    pass

