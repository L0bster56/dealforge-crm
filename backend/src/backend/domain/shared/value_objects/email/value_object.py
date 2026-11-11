import re
from dataclasses import dataclass

from src.backend.domain.shared.value_objects.email.errors import InvalidEmailError


@dataclass(frozen=True)
class Email:
    """
    Email (Value Object).

    Представляет email пользователя и гарантирует его корректность
    на уровне доменной модели.

    Ограничения:
        - значение должно быть строкой;
        - должно соответствовать формату email;
        - приводится к нижнему регистру.

    Attributes:
        value: Значение email.
    """

    value: str

    def __post_init__(self) -> None:
        """
        Валидирует и нормализует email после создания объекта.
        """
        if not isinstance(self.value, str):
            raise InvalidEmailError(self.value)

        if not self.__is_valid():
            raise InvalidEmailError(self.value)

        object.__setattr__(self, "value", self.value.lower())

    def __is_valid(self) -> bool:
        """
        Проверяет корректность формата email.

        Returns:
            True, если email валиден, иначе False.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return re.match(pattern, self.value) is not None

    def __str__(self) -> str:
        """
        Строковое представление email.

        Returns:
            Email в виде строки.
        """
        return self.value