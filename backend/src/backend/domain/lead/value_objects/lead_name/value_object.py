from dataclasses import dataclass

from backend.domain.lead.value_objects.lead_name.errors import UnSupportedLeadNameTypeError, InvalidLeadNameLengthError


@dataclass(frozen=True)
class LeadName:
    """
    VO Name

    Attributes:
        value: Значение в типе данных str
    """
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise UnSupportedLeadNameTypeError()

        if len(self.value) <= 2 or len(self.value) >= 512:
            raise InvalidLeadNameLengthError()

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)
