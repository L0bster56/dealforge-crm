from dataclasses import dataclass

from backend.domain.shared.mixins import IDMixin


@dataclass
class BaseEntity(IDMixin):
    """
    Базовая Сущность

    Attributes:
        id: Уникальный Кодификатор
    """

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: "BaseEntity"):
        return self.id == other.id
