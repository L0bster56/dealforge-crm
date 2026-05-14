from dataclasses import dataclass
import re

from backend.domain.shared.value_objects.phone.error import PhoneFormatError


@dataclass(frozen=True)
class Phone:
    value: str

    def __post_init__(self):
        if not self.__is_valid():
            raise PhoneFormatError("Phone format error")

    def __is_valid(self) -> bool:
        # Очищаем строку от пробелов, скобок и тире
        clean_phone = re.sub(r'[\s\(\)\-]', '', self.value)
        # Регулярное выражение:
        # ^\+          - начинается с плюса
        # [1-9]        - первая цифра кода страны (не ноль)
        # \d{1,3}      - еще до 3-х цифр кода страны
        # \d{5,12}     - от 5 до 12 цифр самого номера
        # $            - конец строки
        pattern = r'^\+[1-9]\d{1,3}\d{5,12}$'
        return bool(re.match(pattern, clean_phone))
