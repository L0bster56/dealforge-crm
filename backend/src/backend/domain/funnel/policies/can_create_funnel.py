from backend.domain.shared.policy import Policy
from backend.domain.user.entity import User, UserRole


class CanCreateFunnelPolicy(Policy):
    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User):
        self._actor = actor

    def _error_message(self) -> str:
        return "You can't create funnel policies directly"

    def is_satisfied_by(self) -> bool:
        return self._actor.role in self.ALLOWED_ROLES
