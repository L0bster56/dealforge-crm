from backend.domain.shared.policy import Policy
from backend.domain.user.entity import User, UserRole


class CanMangeCustomField(Policy):
    ALLOWED_ROLES = {UserRole.admin, UserRole.director}

    def __init__(self, actor: User):
        self._actor = actor

    def is_satisfied_by(self) -> bool:
        return self._actor.role in self.ALLOWED_ROLES

    def _error_message(self) -> str:
        return "You cannot make a custom field of type {}.".format(self._actor.role)
