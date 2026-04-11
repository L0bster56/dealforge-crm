import re
from dataclasses import dataclass

from src.backend.application.auth.errors import WeakPasswordError


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        self._validate()

    def _validate(self):
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
        return self.value == other.value