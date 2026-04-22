from src.backend.domain.shared.errors import DomainError


class ProbabilityError(DomainError):
    pass

class OutOfRangeProbabilityError(ProbabilityError):
    pass

class UnsupportedProbabilityTypeError(ProbabilityError):
    pass