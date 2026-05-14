from backend.application.shared.errors import ApplicationError


class CustomFieldNotFoundError(ApplicationError):
    pass


class CustomFieldNameAlreadyExistsError(ApplicationError):
    pass


class SelectFieldWithoutEnumsError(ApplicationError):
    pass


class EnumInUseError(ApplicationError):
    pass
