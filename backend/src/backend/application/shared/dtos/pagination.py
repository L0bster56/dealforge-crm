from pydantic import BaseModel, Field, computed_field
from typing import TypeVar, Generic, List

T = TypeVar('T')


class PageRequest(BaseModel):
    page: int = Field(ge=1, default=1)
    size: int = Field(ge=1, default=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


class PageResult(BaseModel, Generic[T]):
    items: List[T]
    page: int
    size: int
    total_items: int

    @computed_field
    @property
    def total_pages(self) -> int:
        if self.total_items == 0:
            return 0
        return (self.total_items + self.size - 1) // self.size

    @computed_field
    @property
    def has_next_page(self) -> bool:
        return self.total_pages > self.page

    @computed_field
    @property
    def has_prev_page(self) -> bool:
        return 1 < self.page

    @classmethod
    def empty(cls, page: int = 1, size: int = 50):
        return cls(items=[], page=page, size=size, total_items=0)
