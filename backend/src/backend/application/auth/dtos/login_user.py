from dataclasses import dataclass

from pydantic import BaseModel


class LoginUserCommand(BaseModel):
    """
    команда для авторизации
    """
    username: str
    password: str


class LoginUserResult(BaseModel):
    """
    результат авторизации
    """
    access_token: str
    refresh_token: str
    token_type: str