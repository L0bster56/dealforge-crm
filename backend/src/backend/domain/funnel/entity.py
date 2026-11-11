from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID

from backend.domain.shared.entity import BaseEntity
from backend.domain.shared.mixins import IDMixin, TimeActionMixin
from src.backend.domain.funnel.value_objects.probability.value_object import Probability
from src.backend.domain.shared.value_objects.hex.value_object import HexCode
from src.backend.domain.shared.value_objects.name.value_object import Name


@dataclass
class Funnel(BaseEntity, IDMixin, TimeActionMixin):
    """
    Воронка продаж (Funnel).

    Представляет собой набор этапов, через которые проходит сделка.

    Attributes:
        id: Уникальный идентификатор.
        name: Название воронки (Value Object Name).
        is_deleted: Флаг логического удаления.
    """

    name: Name
    is_deleted: bool = field(default=False)

    @classmethod
    def create(cls, name: str) -> "Funnel":
        """
        Создает новую воронку.

        Args:
            name: Название воронки.

        Returns:
            Экземпляр Funnel.
        """
        return cls(name=Name(name))

    def change_name(self, name: str) -> None:
        """
        Изменяет название воронки.

        Args:
            name: Новое название.
        """
        self.name = Name(name)
        self._touch()

    def delete(self) -> None:
        """
        Помечает воронку как удаленную (soft delete).
        """
        self.is_deleted = True
        self._touch()

    def restore(self):
        self.is_deleted = False
        self._touch()


class StageKind(StrEnum):
    initial = "initial"
    intermediate = "intermediate"
    won = "won"
    lost = "lost"


@dataclass
class FunnelStage(BaseEntity, IDMixin, TimeActionMixin):
    """
    Этап воронки продаж.

    Attributes:
        id: Уникальный идентификатор этапа.
        funnel_id: Идентификатор воронки.
        name: Название этапа (Value Object Name).
        win_probability: Вероятность успеха (Value Object Probability).
        hex_code: Цвет этапа в HEX формате.
        order: Позиция этапа в воронке.
    """

    funnel_id: UUID
    name: Name
    win_probability: Probability
    hex_code: HexCode = field(default_factory=lambda: HexCode("#B255D4"))
    order: int = field(default=0)
    is_archived: bool = field(default=False)
    kind: StageKind = field(default=StageKind.initial)

    @classmethod
    def create(
            cls,
            funnel_id: UUID,
            name: str,
            win_probability: int,
            hex_code: str,
            order: int = 0,
    ) -> "FunnelStage":
        """
        Создает новый этап воронки.

        Args:
            funnel_id: ID воронки.
            name: Название этапа.
            win_probability: Вероятность успеха.
            hex_code: Цвет в HEX формате.
            order: Позиция этапа.

        Returns:
            Экземпляр FunnelStage.
        """
        return cls(
            funnel_id=funnel_id,
            name=Name(name),
            win_probability=Probability(win_probability),
            hex_code=HexCode(hex_code),
            order=order,
        )

    def change_order(self, order: int) -> None:
        """
        Изменяет порядок этапа.

        Args:
            order: Новая позиция.
        """
        if order < 0:
            raise ValueError("Order не может быть отрицательным")

        self.order = order
        self._touch()

    def change(
            self,
            name: str,
            win_probability: int,
            hex_code: str,
    ) -> None:
        """
        Изменяет основные параметры этапа.

        Args:
            name: Новое название.
            win_probability: Новая вероятность.
            hex_code: Новый цвет.
        """
        self.name = Name(name)
        self.win_probability = Probability(win_probability)
        self.hex_code = HexCode(hex_code)
        self._touch()

    def __hash__(self) -> int:
        """
        Хэш по ID.

        Returns:
            Хэш значения.
        """
        return hash(self.id)
