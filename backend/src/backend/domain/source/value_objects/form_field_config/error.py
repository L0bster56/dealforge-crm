from backend.domain.shared.errors import DomainError


class InvalidFormFieldLabelError(DomainError):
    pass

class CustomFieldKindRequiresError(DomainError):
    pass

class FieldIdNotAllowedError(DomainError):
    pass