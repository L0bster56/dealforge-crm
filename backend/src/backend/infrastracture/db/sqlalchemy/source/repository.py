from uuid import UUID

from sqlalchemy import select, and_, exists, Select, func

from backend.application.shared.dtos.pagination import PageResult
from backend.application.source.dtos.list_source import ListSourceCommand, ListSourceSort

from backend.application.source.repository import SourceRepository
from backend.domain.source.entity import Source
from backend.domain.source.enums.source_type.enum import SourceType
from backend.infrastracture.db.sqlalchemy.core.repository import SQLAlchemyRepository
from backend.infrastracture.db.sqlalchemy.source.mapper import to_model, to_entity
from backend.infrastracture.db.sqlalchemy.source.model import SourceModel


class SqlAlchemySourceRepository(SQLAlchemyRepository, SourceRepository):
    _SORT_COLUMNS = {
        ListSourceSort.created_at_asc: SourceModel.created_at.asc(),
        ListSourceSort.created_at_desc: SourceModel.created_at.desc(),
        ListSourceSort.name_asc: SourceModel.name.asc(),
        ListSourceSort.name_desc: SourceModel.name.desc(),
    }

    async def add(self, source: Source) -> Source:
        instance = to_model(source)
        self.session.add(instance)
        await self.session.flush()
        return source

    async def update(self, source: Source) -> Source:
        instance = to_model(source)
        self.session.add(instance)
        await self.session.merge(instance)
        await self.session.flush()
        return source

    async def get_by_id(self, source_id: UUID) -> Source | None:
        stmt = select(SourceModel).where(SourceModel.id == source_id)
        result = await self.session.execute(stmt)
        source = result.scalar_one_or_none()
        return to_entity(source) if source else None

    async def exists_slug(self, slug: str) -> bool:
        condition = and_(
            SourceModel.source_type == "public_form",
            SourceModel.is_deleted.is_(False),
            SourceModel.config["slug"].astext == slug,
        )
        stmt = select(exists().where(condition))

        result = await self.session.execute(stmt)

        return result.scalar()

    async def _count(self, base_stmt: Select) -> int:
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        result = await self.session.execute(count_stmt)
        return result.scalar_one()

    def _apply_filter(
            self,
            stmt: Select,
            source_type: SourceType | None = None,
            is_active: bool | None = None,
            q: str | None = None,
    ) -> Select:
        if source_type is not None:
            stmt = stmt.where(SourceModel.source_type == source_type)
        if is_active is not None:
            stmt = stmt.where(SourceModel.is_active == is_active)
        if q is not None:
            stmt = stmt.where(SourceModel.config.ilike(f"%{q}%"))
        return stmt

    def _apply_sort(
            self,
            stmt: Select,
            sort_by: ListSourceSort | None = None,
    ):
        if sort_by not in self._SORT_COLUMNS:
            return stmt
        return stmt.order_by(self._SORT_COLUMNS[sort_by])

    async def list(self, cmd: ListSourceCommand) -> PageResult[Source]:
        stmt = select(SourceModel)
        stmt = self._apply_filter(
            stmt,
            cmd.type,
            cmd.is_active,
            cmd.q,
        )
        total = await self._count(stmt)

        if total == 0:
            return PageResult.empty()

        stmt = self._apply_sort(
            stmt,
            cmd.sort,
        )

        stmt = stmt.limit(cmd.pagination.limit).offset(cmd.pagination.offset)

        result = await self.session.execute(stmt)

        sources = result.scalars().all()

        return PageResult.paginate(
            items=[to_entity(source) for source in sources],
            total_items=total,
            page=cmd.pagination.page,
            size=cmd.pagination.size
        )
