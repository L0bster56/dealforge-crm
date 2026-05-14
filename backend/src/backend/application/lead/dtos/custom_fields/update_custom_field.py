from pydantic import BaseModel



class UpdateCustomFieldCommand(BaseModel):
    name: str
