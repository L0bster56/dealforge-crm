from pydantic import BaseModel


class ChangePasswordCommand(BaseModel):
    old_password: str
    new_password: str


