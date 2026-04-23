from backend.domain.shared.policy import Policy
from backend.domain.user.entity import User, UserRole


class CanDeleteFunnelPolicy(Policy):
    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User):
        self._actor = actor

    def _error_message(self) -> str:
        return "Can't delete funnel policy for user "

    def is_satisfied_by(self) -> bool:
        return self._actor.role in self.ALLOWED_ROLES