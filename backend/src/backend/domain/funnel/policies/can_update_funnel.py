from backend.domain.shared.policy import Policy
from backend.domain.user.entity import User, UserRole


class CanUpdateFunnelPolicy(Policy):
    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User):
        self._actor = actor

    def _error_message(self) -> str:
        return f"You cannot update funnel policy for"

    def is_satisfied_by(self) -> bool:
        return self._actor in self.ALLOWED_ROLES
