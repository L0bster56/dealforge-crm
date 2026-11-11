import re
from dataclasses import dataclass

from src.backend.domain.user.value_objects.username.errors import (
    InvalidUsernameLengthError,
    InvalidUsernameFormatError,
    UnSupportedUsernameTypeError,
)


@dataclass(frozen=True)
class Username:
    """
    Username (Value Object).

    Представляет уникальное имя пользователя в системе и гарантирует его корректность
    на уровне доменной модели.

    Правила валидации:
        - значение должно быть строкой;
        - длина от 4 до 255 символов;
        - первый символ должен быть буквой;
        - допускаются только латинские буквы, цифры и символ "_";
        - приводится к нижнему регистру.

    Attributes:
        value: Значение username.
    """

    value: str

    def __post_init__(self) -> None:
        """
        Валидирует и нормализует username после создания объекта.
        """
        if not isinstance(self.value, str):
            raise UnSupportedUsernameTypeError()

        if len(self.value) <= 3 or len(self.value) > 255:
            raise InvalidUsernameLengthError()

        if not self.__is_valid():
            raise InvalidUsernameFormatError()

        object.__setattr__(self, "value", self.value.lower())

    def __is_valid(self) -> bool:
        """
        Проверяет соответствие username допустимому формату.

        Returns:
            True, если username соответствует шаблону, иначе False.
        """
        pattern = r"^[a-zA-Z][a-zA-Z0-9_]*$"
        return re.match(pattern, self.value) is not None

    def __str__(self) -> str:
        """
        Строковое представление username.

        Returns:
            Username в виде строки.
        """
        return self.value
