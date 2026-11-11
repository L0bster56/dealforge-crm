from enum import StrEnum


class SourceType(StrEnum):
    manual = "manual"
    webhook = "webhook"
    public_form = "public_form"
