from src.backend.application.shared.errors import ApplicationError, ConflictError, NotFoundError


class UserError(ApplicationError):
    pass

class UserNotFoundError(NotFoundError, UserError):
    pass

class UsernameAlreadyExistsError(ConflictError, UserError):
    pass