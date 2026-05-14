from pydantic import BaseModel


class AddEnumValueCommand(BaseModel):
    value: str
