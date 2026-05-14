from dataclasses import dataclass

from backend.domain.lead.value_objects.contact.errors import ContactError
from backend.domain.shared.value_objects.email.value_object import Email
from backend.domain.shared.value_objects.name.value_object import Name
from backend.domain.shared.value_objects.phone.value_object import Phone


@dataclass(frozen=True)
class Contact:
    full_name: Name
    email: Email | None = None
    phone: Phone | None = None
    telegram: str | None = None

    def __post_init__(self):
        if not (self.email or self.phone or self.telegram):
            raise ContactError("At least one of email, phone or telegram is required")
