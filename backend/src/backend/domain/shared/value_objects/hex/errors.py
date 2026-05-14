from src.backend.domain.shared.errors import DomainError


class HexError(DomainError):
    """
    Базовая ошибка для Value Object HexCode.
    """


class InvalidHexError(HexError):
    """
    Ошибка некорректного HEX-кода.
    """


class UnsupportedHexTypeError(HexError):
    """
    Ошибка неподдерживаемого типа HEX-кода.
    """
