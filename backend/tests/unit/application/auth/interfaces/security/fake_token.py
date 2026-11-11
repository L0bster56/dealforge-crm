from src.backend.application.auth.interfaces.security.token import TokenService


class FakeTokenService(TokenService):
    def __init__(self, data: dict = None):
        self._data = data

    def encode(self, data: dict) -> str:
        return f"token: {data.get('sub')}"

    def decode(self, token: str) -> dict:
        return self._data

    def get_token_type(self) -> str:
        return "Bearer"