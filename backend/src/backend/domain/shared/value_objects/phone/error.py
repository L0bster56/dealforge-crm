from backend.domain.shared.errors import DomainError


class PhoneError(DomainError):
    pass


class PhoneFormatError(PhoneError):
    pass
