import re
from dataclasses import dataclass

from backend.domain.shared.value_objects.email.errors import InvalidEmailError


@dataclass(frozen=True)
class Email:
    """
    VO Email нужен для полей в которых будет электронная почта

    Attributes:
        value (str): Значение в типе данных str
    """
    value: str

    def __post_init__(self):
        if not self.__is_valid():
            raise InvalidEmailError()


    def __is_valid(self):
        """
        Приватная Функция для проверки валидного еmаil

        :return:
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return re.match(pattern, self.value) is not None
