from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse

from src.backend.application.shared.errors import BadRequestError


async def bad_request_exception_handler(reqeust: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "status_code": status.HTTP_400_BAD_REQUEST
        }
    )