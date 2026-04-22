from dataclasses import dataclass

from src.backend.domain.funnel.value_objects.probability.errors import OutOfRangeProbabilityError, \
    UnsupportedProbabilityTypeError


@dataclass(frozen=True)
class Probability:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise UnsupportedProbabilityTypeError()

        if not self.__validate():
            raise OutOfRangeProbabilityError()

    def __validate(self) -> bool:
        return 0 <= self.value <= 100