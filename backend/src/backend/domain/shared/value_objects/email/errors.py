from backend.domain.shared.errors import DomainError


class EmailError(DomainError):
    """
    Базовая Ошибка VO Email
    """

class InvalidEmailError(EmailError):
    """
    Вызывается когда неправильный форма Жектронной почты
    """

