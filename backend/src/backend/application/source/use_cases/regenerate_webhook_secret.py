from dataclasses import dataclass

from backend.application.shared.interfaces.uow import UnitOfWork
from backend.application.source.dtos.regenerate_webhook_secret import RegenerateWebhookSecretResult
from backend.domain.source.entity import Source
from backend.domain.source.enums.source_type.enum import SourceType
from backend.domain.source.error import NotWebhookSourceError
from backend.domain.user.entity import User


@dataclass
class RegenerateWebhookSecretUseCase:
    uow: UnitOfWork
    user: User
    source: Source

    async def execute(self):
        if self.source.source_type != SourceType.webhook:
            raise NotWebhookSourceError()

        token = self.source.regenerate_secret()
        async with self.uow:
            await self.uow.sources.update(self.source)
            await self.uow.commit()
        return RegenerateWebhookSecretResult(
            secret_token=token,
        )