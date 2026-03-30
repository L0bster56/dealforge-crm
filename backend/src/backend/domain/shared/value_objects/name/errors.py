from backend.domain.shared.errors import DomainError


class NameErrors(DomainError):
    """

    """

class UnsupportedNameTypeError(NameErrors):
    """

    """

class InvalidNameLengthError(NameErrors):
    """

    """

class InvalidNameFormatError(NameErrors):
    """

    """