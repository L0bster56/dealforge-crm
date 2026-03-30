from backend.domain.shared.errors import DomainError


class UsernameError(DomainError):
    """
    Базовая ошибка VO Username
    """


class UnSupportedUsernameTypeError(UsernameError):
    """
    Вызывается когда указали неправильный тип значения
    """


class InvalidUsernameLengthError(UsernameError):
    """
    Вызывается когда длина имени пользователя превышает диапазон
    """


class InvalidUsernameFormatError(UsernameError):
    """
    Вызывается когда формат имени пользователя неправильный
    """
