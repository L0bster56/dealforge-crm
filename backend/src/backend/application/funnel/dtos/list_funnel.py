from enum import StrEnum

from pydantic import BaseModel

from backend.application.shared.dtos.pagination import PageResult


class FunnelSortEnum(StrEnum):
    name_asc = 'name:asc'
    name_desc = 'name:desc'
    created_at_desc = 'created_at:desc'
    created_at_asc = 'created_at:asc'


class ListFunnelCommand(BaseModel):
    q: str | None = None
    sort_by: str | None = None
    pagination: PageResult
