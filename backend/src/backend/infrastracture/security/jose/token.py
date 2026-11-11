from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from jose import jwt, JWTError
from src.backend.application.auth.interfaces.security.token import TokenService
from src.backend.config import get_settings

settings = get_settings()


class JWTTokenService(TokenService):
    def encode(self, user_id: UUID, is_refresh: bool = False) -> str:
        payload: dict[str, Any] = {
            "sub": str(user_id)
        }
        if is_refresh:
            exp_td = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES)
        else:
            exp_td = timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES)

        payload["exp"] = datetime.now(tz=timezone.utc) + exp_td
        payload["is_refresh"] = is_refresh

        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

    def decode(self, token: str, is_refresh: bool = False) -> UUID:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload.get("is_refresh") is None:
            raise JWTError
        if (payload.get("is_expired") and not is_refresh) or (not payload.get("is_refresh") and is_refresh):
            raise JWTError("Invalid token")

        return UUID(payload["sub"])

    def get_token_type(self) -> str:
        return "Bearer"
