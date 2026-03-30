from datetime import datetime
import uuid
from dataclasses import dataclass, field

from backend.domain.shared.value_objects.email.value_object import Email
from backend.domain.shared.value_objects.name.value_object import Name
from backend.domain.user.value_objects.username.value_object import Username


@dataclass
class User:
    id: uuid.UUID
    first_name: Name
    last_name: Name
    username: Username
    email: Email
    password_hash: str
    last_interaction: datetime
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    update_at: datetime = field(default_factory=datetime.now)
