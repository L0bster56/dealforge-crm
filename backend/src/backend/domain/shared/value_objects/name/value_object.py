import re
from dataclasses import dataclass

from backend.domain.shared.value_objects.name.errors import UnsupportedNameTypeError, InvalidNameLengthError, \
    InvalidNameFormatError


@dataclass
class Name:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise UnsupportedNameTypeError()

        value = self.value.strip()

        if len(value) <= 2 or len(value) > 255:
            raise InvalidNameLengthError()

        if not self.__is_valid(value):
            raise InvalidNameFormatError()

        object.__setattr__(self, "value", value)

    def __is_valid(self, value: str) -> bool:
        pattern = r"^[a-zA-Zа-яА-ЯёЁ]+([ -][a-zA-Zа-яА-ЯёЁ]+)*$"
        return re.match(pattern, value) is not None
