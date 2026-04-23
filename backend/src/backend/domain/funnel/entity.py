from _datetime import datetime
from dataclasses import dataclass, field
from uuid import UUID

from src.backend.domain.funnel.value_objects.probability.value_object import Probability
from src.backend.domain.shared.value_objects.hex.value_object import HexCode
from src.backend.domain.shared.value_objects.name.value_object import Name


@dataclass
class Funnel:
    id: UUID
    name: Name
    is_deleted: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.now)
    update_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(
            cls,
            id: UUID,
            name: str
    ):
        return cls(
            id=id,
            name=Name(name)
        )

    def _touch(self) -> None:
        self.update_at = datetime.now()

    def change_name(self, name: str):
        self.name = Name(name)
        self._touch()

    def delete(self):
        self.is_deleted = True
        self._touch()


@dataclass
class FunnelStage:
    id: UUID
    funnel_id: UUID
    name: Name
    win_probability: Probability
    hex: HexCode = field(default=HexCode("#B255D4"))
    order: int = field(default=0)

    @classmethod
    def create(
            cls,
            id: UUID,
            funnel_id: UUID,
            name: str,
            win_probability: int,
            hex: str,
            order: int,
    ):
        return cls(
            id=id,
            funnel_id=funnel_id,
            name=Name(name),
            win_probability=Probability(win_probability),
            hex=HexCode(hex),
            order=order
        )
