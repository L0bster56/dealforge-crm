from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, UUID

from src.backend.infrastracture.db.sqlalchemy.core.mixins import UUIDMixin, TimeStampMixin
from src.backend.infrastracture.db.sqlalchemy.core.models import Base


class FunnelModel(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'funnels'

    name = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)


class FunnelStageModel(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'funnel_stages'

    name = Column(String(255), nullable=False)
    funnel_id = Column(UUID, ForeignKey('funnels.id', ondelete="CASCADE"), nullable=False)
    win_probability = Column(Integer, nullable=False)
    hex = Column(String(7), nullable=False)
    order = Column(Integer, nullable=False)
    is_archived = Column(Boolean, nullable=True, default=False)
    kind = Column(String(100), nullable=True, default="initial")
