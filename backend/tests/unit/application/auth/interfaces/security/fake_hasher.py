from src.backend.application.auth.interfaces.security.hasher import Hasher


class FakeHasher(Hasher):
    def __init__(self, result=True):
        self._result = result

    def hash(self, password: str) -> str:
        return f"hash:{password}"

    def verify(self, password: str, hashed_password: str) -> bool:
        return self._result