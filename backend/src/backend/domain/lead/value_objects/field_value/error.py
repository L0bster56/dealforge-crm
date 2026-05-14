from backend.domain.shared.errors import DomainError


class FieldValueError(DomainError):
    pass

class EmptyFieldValueError(FieldValueError):
    pass

class MultipleFieldValueError(FieldValueError):
    pass
