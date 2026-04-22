from pydantic import BaseModel, EmailStr


class UpdateMeCommand(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


