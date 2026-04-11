from src.backend.domain.shared.errors import DomainError


class IdError(DomainError):
    """
    Базовая ошибка VO Id
    """

class UnsupportedTypeIdError(IdError):
    """
    Вызывается когда дают не поддерживающий тип значения
    """


class NegativeIntIdError(IdError):
    """
    Вызывается когда дают отрицательное значение
    """

