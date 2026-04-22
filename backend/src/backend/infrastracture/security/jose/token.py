from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt
from src.backend.application.auth.interfaces.security.token import TokenService
from src.backend.config import get_settings

settings = get_settings()

class JWTTokenService(TokenService):
    def encode(self, user_id: UUID, is_refresh: bool = False) -> str:
        payload = {
            "sub": str(user_id)
        }
        if is_refresh:
            exp_td = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES)
        else:
            exp_td = timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES)

        payload["exp"] = datetime.now() + exp_td

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
        return UUID(payload["sub"])



    def get_token_type(self) -> str:
        return "Bearer"

