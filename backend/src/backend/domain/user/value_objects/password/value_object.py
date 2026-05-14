import re
from dataclasses import dataclass

from src.backend.application.auth.errors import WeakPasswordError


@dataclass(frozen=True)
class Password:
    """
    Value Object для представления пароля.

    Обеспечивает валидацию сложности пароля согласно требованиям безопасности.

    Attributes:
        value (str): Строковое значение пароля.
    """

    value: str

    def __post_init__(self):
        """
        Запускает валидацию пароля после создания объекта.

        Raises:
            WeakPasswordError: Если пароль не соответствует требованиям.
        """
        self._validate()

    def _validate(self):
        """
        Проверяет пароль на соответствие требованиям:

        - Минимум 8 символов
        - Хотя бы одна заглавная буква
        - Хотя бы одна строчная буква
        - Хотя бы одна цифра
        - Хотя бы один специальный символ

        Raises:
            WeakPasswordError: Если любое из условий не выполнено.
        """
        v = self.value

        if len(v) < 8:
            raise WeakPasswordError("Пароль должен содержать минимум 8 символов")

        if not re.search(r"[A-Z]", v):
            raise WeakPasswordError("Пароль должен содержать хотя бы одну заглавную букву")

        if not re.search(r"[a-z]", v):
            raise WeakPasswordError("Пароль должен содержать хотя бы одну строчную букву")

        if not re.search(r"\d", v):
            raise WeakPasswordError("Пароль должен содержать хотя бы одну цифру")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise WeakPasswordError("Пароль должен содержать хотя бы один специальный символ")

    def is_same_as(self, other: "Password") -> bool:
        """
        Сравнивает текущий пароль с другим.

        Args:
            other (Password): Другой пароль для сравнения.

        Returns:
            bool: True если пароли совпадают, иначе False.
        """
        return self.value == other.value
