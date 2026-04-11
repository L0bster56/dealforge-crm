from dataclasses import dataclass
from uuid import UUID



@dataclass(frozen=True)
class ChangePasswordCommand:
    user_id: UUID
    old_password: str
    new_password: str