from src.backend.application.shared.errors import ApplicationError


class AuthError(ApplicationError):
    """
    Базовая ошибка Auth
    """

class AuthUserNotFoundError(AuthError):
    pass

class InvalidPasswordError(AuthError):
    pass

class InActiveUserError(AuthError):
    pass

class WeakPasswordError(AuthError):
    pass

class SamePasswordError(AuthError):
    pass
