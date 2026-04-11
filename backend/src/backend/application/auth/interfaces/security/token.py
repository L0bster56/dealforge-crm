from typing import Protocol

class TokenService(Protocol):
    """
    Interface сервиса токенов
    """
    def encode(self, data: dict) -> str: ...

    def decode(self, token: str) -> dict: ...

    def get_token_type(self) -> str: ...