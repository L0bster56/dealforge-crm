from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse

from src.backend.application.shared.errors import BadRequestError


async def conflict_exception_handler(reqeust: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
            "status_code": status.HTTP_409_CONFLICT
        }
    )