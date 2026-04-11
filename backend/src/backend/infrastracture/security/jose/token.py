from datetime import datetime, timedelta

from jose import jwt
from src.backend.application.auth.interfaces.security.token import TokenService
from src.backend.config import get_settings

settings = get_settings()

class JWTTokenService(TokenService):
    def encode(self, data: dict) -> str:

        payload = data
        if payload.get("is_refresh"):
            exp_td = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES)
        else:
            exp_td = timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES)

        payload["exp"] = datetime.now () + exp_td

        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )


    def decode(self, token: str) -> dict:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

    def get_token_type(self) -> str:
        return "Bearer"

