from uuid import UUID

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from backend.application.funnel.dtos.list_funnel import ListFunnelCommand, FunnelSortEnum
from backend.application.funnel.repository import FunnelRepository
from backend.application.shared.dtos.pagination import PageResult
from backend.domain.funnel.entity import Funnel
from backend.infrastracture.db.sqlalchemy.funnel.models import FunnelModel


def to_entity(funnel: Funnel) -> Funnel:
    return Funnel(
        id=funnel.id,
        name=funnel.name,
        is_deleted=funnel.is_deleted,
        created_at=funnel.created_at,
        update_at=funnel.update_at,
    )


def to_model(funnel: Funnel) -> FunnelModel:
    return FunnelModel(
        id=funnel.id,
        name=funnel.name.value,
        is_deleted=bool(funnel.is_deleted),
        created_at=funnel.created_at,
        updated_at=funnel.updated_at,
    )


class SqlAlchemyFunnelRepository(FunnelRepository):
    _SORT_COLUMNS = {
        FunnelSortEnum.name_asc: FunnelModel.name.asc(),
        FunnelSortEnum.name_desc: FunnelModel.name.desc(),
        FunnelSortEnum.created_at_asc: FunnelModel.name.asc(),
        FunnelSortEnum.created_at_desc: FunnelModel.name.desc(),
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_funnel(self, funnel: Funnel) -> Funnel:
        instance = to_model(funnel)
        self.session.add(instance)
        await self.session.flush()
        return to_entity(instance)

    async def update_funnel(self, funnel: Funnel) -> Funnel:
        instance = to_model(funnel)
        self.session.add(instance)
        await self.session.flush()
        return to_entity(instance)

    async def delete_funnel(self, funnel: Funnel) -> None:
        instance = to_model(funnel)
        self.session.add(instance)
        await self.session.flush()

    async def get_funnel_by_id(self, funnel_id: UUID) -> Funnel | None:
        stmt = select(FunnelModel).where(FunnelModel.id == funnel_id)
        result = await self.session.execute(stmt)
        funnel = result.scalar_one_or_none()
        return to_entity(funnel) if funnel else None

    def _apply_filters(self, stmt: Select, q: str | None = None) -> Select:
        if q:
            stmt = stmt.where(FunnelModel.name.ilike(f"%{q}%"))
        return stmt

    def __apply_sort(self, stmt: Select, sort_by: FunnelSortEnum | None = None) -> Select:
        if not sort_by in self._SORT_COLUMNS:
            return stmt
        return stmt.order_by(self._SORT_COLUMNS[sort_by])

    async def _count(self, base_stmt: Select) -> int:
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        result = await self.session.execute(count_stmt)
        return result.scalar_one()

    async def get_funnels(self, cmd: ListFunnelCommand) -> PageResult[Funnel]:
        stmt = select(FunnelModel)
        stmt = self._apply_filters(stmt, cmd.q)

        total = await self._count(stmt)

        if total == 0:
            return PageResult.empty()

        stmt = self.__apply_sort(stmt, cmd.sort_by)
        stmt = stmt.offset(cmd.offset).limit(cmd.limit).offset(cmd.pagination.offset)
        result = await self.session.execute(stmt)
        funnels = result.scalars().all()

        return PageResult(
            items=[to_entity(funnels) for funnels in funnels],
            total_items=total,
            page=cmd.pagination.page,
            size=cmd.pagination.page_size,
        )
