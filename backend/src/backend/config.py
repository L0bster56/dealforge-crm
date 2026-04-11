from anyio.functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    #Postgres DB
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_NAME: str
    POSTGRES_HOST : str
    POSTGRES_PORT : int

    # JWT
    JWT_SECRET : str
    JWT_ACCESS_TOKEN_EXPIRES: int
    JWT_REFRESH_TOKEN_EXPIRES : int
    JWT_ALGORITHM : str

@lru_cache
def get_settings() -> Settings:
    return Settings()