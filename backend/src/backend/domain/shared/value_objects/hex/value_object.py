import re
from dataclasses import dataclass

from src.backend.domain.shared.value_objects.hex.errors import InvalidHexError, UnsupportedHexTypeError


@dataclass(frozen=True)
class HexCode:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise UnsupportedHexTypeError()

        if not self.__validate():
            raise InvalidHexError()

    def __validate(self) -> bool:
        return bool(re.match(r"^#[0-9A-Fa-f]{6}$", self.value))

    def __str__(self):
        return self.value