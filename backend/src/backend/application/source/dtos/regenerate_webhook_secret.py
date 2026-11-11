from pydantic import BaseModel


class RegenerateWebhookSecretResult(BaseModel):
    secret_token: str