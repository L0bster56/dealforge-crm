from pydantic import BaseModel


class RefreshTokenCommand(BaseModel):
    refresh_token: str


class RefreshTokenResult(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
