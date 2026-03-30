from src.backend.domain.shared.errors import DomainError


class IDError(DomainError):
    """
    Это Базовая ошибка VO Id
    """

class UnsupportedTypeIdError(IDError):
    """
    Вызывается когда дают не поддерживающий тип значения.
    """

class NegativeIntIdError(IDError):
    """
    Вызывается когда дают отрицательное значение.
    """