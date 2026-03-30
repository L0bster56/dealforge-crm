from datetime import datetime
import uuid
from dataclasses import dataclass, field

from backend.domain.shared.value_objects.email.value_object import Email


@dataclass
class User:
    id: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: Email
    password_hash: str
    last_interaction: datetime
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    update_at: datetime = field(default_factory=datetime.now)
