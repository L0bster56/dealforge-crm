from backend.application.shared.errors import ApplicationError


class NotWebhookSourceError(ApplicationError):
    pass

class SourceNotFoundError(ApplicationError):
    pass

class SlugAlreadyError(ApplicationError):
    pass

class AssignmentPoolInvalidRoleError(ApplicationError):
    pass

class CanNotSourceTypeError(ApplicationError):
    pass