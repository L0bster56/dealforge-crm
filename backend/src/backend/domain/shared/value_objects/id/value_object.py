from dataclasses import dataclass

from src.backend.domain.shared.value_objects.id.errors import UnsupportedTypeIdError, NegativeIntIdError


@dataclass(frozen=True)
class Id:
    """
    VO Id нужен для значений целочисленных ИД

    Attributes:
        value: Значение в типе данных int
    """
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise UnsupportedTypeIdError()

        if self.value <= 0:
            raise NegativeIntIdError
