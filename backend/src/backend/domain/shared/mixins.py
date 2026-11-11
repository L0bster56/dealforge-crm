import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from uuid import UUID


@dataclass(kw_only=True)
class IDMixin:
    """
    Mixin для уникальных индикаторов для Entity

    Attributes:
        id: Уникальный Кодификатор
    """
    id: UUID = field(default_factory=uuid.uuid4)


@dataclass(kw_only=True)
class TimeActionMixin:
    """
    Mixin для временных меток для Entity

    Attributes:
        created_at: Временная метка создания
        updated_at: Временная метка обновления
    """
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))

    def _touch(self) -> None:
        """
        Будет фиксировать время изменения
        :return:
        """
        self.update_at = datetime.now(tz=timezone.utc)
