import re
from dataclasses import dataclass

from src.backend.domain.shared.value_objects.name.errors import UnSupportedNameTypeError, InvalidNameLengthError, \
    InvalidNameFormatError


@dataclass(frozen=True)
class Name:
    """
    VO Name

    Attributes:
        value: Значение в типе данных str
    """
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise UnSupportedNameTypeError()

        if len(self.value) <= 2 or len(self.value) >= 255:
            raise InvalidNameLengthError()

        if not self.__is_valid():
            raise InvalidNameFormatError()


    def __is_valid(self) -> bool:
        """
        Приватная функция для проверки валидного имени
        :return: True или False
        """
        pattern = r'^[a-zA-Zа-яА-ЯёЁ]+$'
        return re.match(pattern, self.value) is not None

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)