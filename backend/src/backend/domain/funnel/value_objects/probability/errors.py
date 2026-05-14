from src.backend.domain.shared.errors import DomainError


class ProbabilityError(DomainError):
    """
    Базовая ошибка для Value Object Probability.
    """


class OutOfRangeProbabilityError(ProbabilityError):
    """
    Ошибка, возникающая при выходе значения вероятности за допустимый диапазон.
    """


class UnsupportedProbabilityTypeError(ProbabilityError):
    """
    Ошибка, возникающая при передаче неподдерживаемого типа.
    """
