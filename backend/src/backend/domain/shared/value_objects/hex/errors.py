from src.backend.domain.shared.errors import DomainError


class HexError(DomainError):
    pass

class InvalidHexError(HexError):
    pass

class UnsupportedHexTypeError(HexError):
    pass