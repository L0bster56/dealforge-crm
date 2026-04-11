from src.backend.application.auth.errors import WeakPasswordError
from tests.unit.domain.shared.specification import Specification, T


class PasswordLengthSpecification(Specification[str]):
    def is_satisfied_by(self,password: str) -> bool:
        return len(password) >= 8

class PasswordUpperLetterSpecification(Specification[str]):
    def is_satisfied_by(self,password: str) -> bool:
        return any(c.isupper() for c in password)

class PasswordLowerLetterSpecification(Specification[str]):
    def is_satisfied_by(self, password: str) -> bool:
        return any(c.islower() for c in password)

class PasswordDigitSpecification(Specification[str]):
    def is_satisfied_by(self, password: str) -> bool:
        return any(c.isdigit() for c in password)
class PasswordSpecialCharacterSpecification(Specification[str]):
    SPECIAL = set("!@#$%^&*()_+-=[]{}|;:'\"\\,.<>/?`~")

    def is_satisfied_by(self, password: str) -> bool:
        return any(c in self.SPECIAL for c in password)

class PasswordDifferenceSpecification(Specification[tuple[str, str]]):
    def is_satisfied_by(self, passwords: tuple[str,str]) -> bool:
        old_password, new_password = passwords
        return old_password != new_password


# l = PasswordLengthSpecification()
# u = PasswordUpperLetterSpecification()
# combo = l & u
#
# print(l.is_satisfied_by("Jaxanqir"))
# print(u.is_satisfied_by("Jaxanqir"))
# print(type(combo))
# print(combo.is_satisfied_by("Jaxanqir"))
# print(combo.is_satisfied_by("Malika"))