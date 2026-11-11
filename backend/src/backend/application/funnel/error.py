from backend.application.shared.errors import ApplicationError


class StageNotFunnelError(ApplicationError):
    pass

class FunnelNotFoundError(ApplicationError):
    pass