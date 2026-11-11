import re
from dataclasses import dataclass

from src.backend.domain.shared.value_objects.hex.errors import (
    InvalidHexError,
    UnsupportedHexTypeError,
)


@dataclass(frozen=True)
class HexCode:
    """
    HexCode (Value Object).

    Представляет цвет в формате HEX и гарантирует его корректность.

    Ограничения:
        - значение должно быть строкой;
        - формат строго: #RRGGBB;
        - допускаются только шестнадцатеричные символы;
        - приводится к верхнему регистру.

    Attributes:
        value: HEX-строка цвета.
    """

    value: str

    def __post_init__(self) -> None:
        """
        Валидирует и нормализует HEX-код.
        """
        if not isinstance(self.value, str):
            raise UnsupportedHexTypeError(self.value)

        if not self.__is_valid():
            raise InvalidHexError(self.value)

        object.__setattr__(self, "value", self.value.upper())

    def __is_valid(self) -> bool:
        """
        Проверяет корректность HEX-формата.

        Returns:
            True, если формат валиден, иначе False.
        """
        pattern = r"^#[0-9A-Fa-f]{6}$"
        return re.match(pattern, self.value) is not None

    def __str__(self) -> str:
        """
        Строковое представление HEX-кода.

        Returns:
            HEX-строка.
        """
        return self.value