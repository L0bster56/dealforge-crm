from src.backend.domain.shared.errors import DomainError


class LeadNameVOError(DomainError):
    """
    Базовая ошибка VO Lead Name
    """


class UnSupportedLeadNameTypeError(LeadNameVOError):
    """
    Вызывается когда указали неправильный тип значения
    """


class InvalidLeadNameLengthError(LeadNameVOError):
    """
    Вызывается когда длина имени превышает диапазон
    """
