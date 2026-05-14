from src.backend.domain.shared.specification import Specification, T


class PasswordLengthSpecification(Specification[str]):
    """
    Спецификация проверки минимальной длины пароля.

    Условие:
        Пароль должен содержать не менее 8 символов.
    """

    def is_satisfied_by(self, password: str) -> bool:
        """
        Проверяет длину пароля.

        Args:
            password (str): Пароль для проверки.

        Returns:
            bool: True если длина >= 8, иначе False.
        """
        return len(password) >= 8


class PasswordUpperLetterSpecification(Specification[str]):
    """
    Спецификация проверки наличия заглавной буквы.

    Условие:
        Пароль должен содержать хотя бы одну заглавную букву.
    """

    def is_satisfied_by(self, password: str) -> bool:
        """
        Проверяет наличие заглавной буквы.

        Args:
            password (str): Пароль для проверки.

        Returns:
            bool: True если есть заглавная буква, иначе False.
        """
        return any(c.isupper() for c in password)


class PasswordLowerLetterSpecification(Specification[str]):
    """
    Спецификация проверки наличия строчной буквы.

    Условие:
        Пароль должен содержать хотя бы одну строчную букву.
    """

    def is_satisfied_by(self, password: str) -> bool:
        """
        Проверяет наличие строчной буквы.

        Args:
            password (str): Пароль для проверки.

        Returns:
            bool: True если есть строчная буква, иначе False.
        """
        return any(c.islower() for c in password)


class PasswordDigitSpecification(Specification[str]):
    """
    Спецификация проверки наличия цифры.

    Условие:
        Пароль должен содержать хотя бы одну цифру.
    """

    def is_satisfied_by(self, password: str) -> bool:
        """
        Проверяет наличие цифры.

        Args:
            password (str): Пароль для проверки.

        Returns:
            bool: True если есть цифра, иначе False.
        """
        return any(c.isdigit() for c in password)


class PasswordSpecialCharacterSpecification(Specification[str]):
    """
    Спецификация проверки наличия специального символа.

    Условие:
        Пароль должен содержать хотя бы один специальный символ.
    """

    SPECIAL = set("!@#$%^&*()-_+=/{}[];:'\"\\|`~?,.")

    def is_satisfied_by(self, password: T) -> bool:
        """
        Проверяет наличие специального символа.

        Args:
            password (str): Пароль для проверки.

        Returns:
            bool: True если есть спецсимвол, иначе False.
        """
        return any(c in self.SPECIAL for c in password)


class PasswordDifferenceSpecification(Specification[tuple[str, str]]):
    """
    Спецификация проверки различия паролей.

    Условие:
        Новый пароль не должен совпадать со старым.
    """

    def is_satisfied_by(self, passwords: tuple[str, str]) -> bool:
        """
        Проверяет, отличаются ли пароли.

        Args:
            passwords (tuple[str, str]): Кортеж (старый пароль, новый пароль).

        Returns:
            bool: True если пароли разные, иначе False.
        """
        old_password, new_password = passwords
        return old_password != new_password