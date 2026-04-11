from dataclasses import dataclass

@dataclass(frozen=True)
class LoginUserCommand:
    """
    Команда для авторизации
    """
    username: str
    password: str

@dataclass(frozen=True)
class LoginUserResult:
    """
    Результат авторизации
    """
    access_token: str
    refresh_token: str
    token_type: str