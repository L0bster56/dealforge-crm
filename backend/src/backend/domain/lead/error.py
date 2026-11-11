from backend.domain.shared.value_objects.errors import DomainError


class FieldTypeNotSelectError(DomainError):
    pass


class EnumValueAlreadyExistsError(DomainError):
    pass

class InvalidEnumIdError(DomainError):
    pass
