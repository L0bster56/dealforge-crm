from backend.application.shared.errors import ApplicationError


class StageNotFunnelError(ApplicationError):
    pass


class StageNotFoundError(ApplicationError):
    pass

class StageNotInFunnelError(ApplicationError):
    pass