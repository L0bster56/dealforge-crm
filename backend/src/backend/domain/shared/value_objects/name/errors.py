from src.backend.domain.shared.errors import DomainError


class NameVOError(DomainError):
    """
    Базовая ошибка VO Name
    """

class UnSupportedNameTypeError(NameVOError):
    """
    Вызывается когда указали неправильный тип значения
    """

class InvalidNameLengthError(NameVOError):
    """
    Вызывается когда длина имени превышает диапазон
    """

class InvalidNameFormatError(NameVOError):
    """
    Вызывается когда формат имени неправильный
    """