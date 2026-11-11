from dataclasses import dataclass

from src.backend.domain.funnel.value_objects.probability.errors import (
    OutOfRangeProbabilityError,
)


@dataclass(frozen=True)
class Probability:
    """
    Probability (Value Object).

    Представляет вероятность успеха этапа воронки в процентах.

    Ограничения:
        - значение должно быть целым числом;
        - диапазон: от 0 до 100 включительно.

    Attributes:
        value: Значение вероятности.
    """

    value: int

    def __post_init__(self) -> None:
        """
        Валидирует значение вероятности после инициализации.
        """

        if not self.__validate():
            raise OutOfRangeProbabilityError()

    def __validate(self) -> bool:
        """
        Проверяет, находится ли значение в допустимом диапазоне.

        Returns:
            True, если значение от 0 до 100, иначе False.
        """
        return 0 <= self.value <= 100

    def __int__(self) -> int:
        """
        Преобразует объект в целое число.

        Returns:
            Значение вероятности.
        """
        return self.value

