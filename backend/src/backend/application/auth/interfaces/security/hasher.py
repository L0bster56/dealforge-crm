from typing import Protocol

class Hasher(Protocol):
    """
    Interface Для хеширования
    """
    def hash(self, password: str) -> str: ...

    def verify(self, password: str, hashed_password) -> bool: ...