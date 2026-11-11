from fastapi import Request
from jose import JWTError
from starlette import status
from starlette.responses import JSONResponse

from src.backend.application.auth.errors import NotAuthorizedError


async def not_authorized_exception_handler(request: Request, exc: NotAuthorizedError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": str(exc),
            "status_code": status.HTTP_401_UNAUTHORIZED
        }
    )


async def token_exception_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Invalid credentials",
            "status_code": status.HTTP_401_UNAUTHORIZED
        }
    )