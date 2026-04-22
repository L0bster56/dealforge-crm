from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse

from src.backend.application.shared.errors import NotFoundError


async def not_found_exception_handler(reqeust: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
            "status_code": status.HTTP_404_NOT_FOUND
        }
    )