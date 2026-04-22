from fastapi import FastAPI
from jose import JWTError

from src.backend.application.auth.errors import InvalidPasswordError, NotAuthorizedError
from src.backend.application.shared.errors import BadRequestError, ConflictError, NotFoundError
from src.backend.presentation.api.v1.auth.router import router as auth_router
from src.backend.presentation.api.v1.core.handlers.auth import not_authorized_exception_handler, token_exception_handler
from src.backend.presentation.api.v1.core.handlers.bad_request import bad_request_exception_handler
from src.backend.presentation.api.v1.core.handlers.conflict import conflict_exception_handler
from src.backend.presentation.api.v1.core.handlers.not_found import not_found_exception_handler
from src.backend.presentation.api.v1.user.router import router as user_router
app = FastAPI(
    title="DealForge CRM API",
    description="",
    version="1.0.0"
)

app.add_exception_handler(NotAuthorizedError, not_authorized_exception_handler)
app.add_exception_handler(JWTError, token_exception_handler)
app.add_exception_handler(BadRequestError, bad_request_exception_handler)
app.add_exception_handler(ConflictError, conflict_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)


# {
#   "first_name": "user1",
#   "last_name": "test",
#   "username": "user1",
#   "email": "user1@test.com",
#   "password": "User1Test@",
#   "role": "consultant"
# }